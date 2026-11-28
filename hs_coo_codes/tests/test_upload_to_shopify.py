"""
Test uploading codes to Shopify. The Shopify API is mocked, so no requests reach the store.
"""

import csv
import logging

import pytest
import requests

from hs_coo_codes import upload_to_shopify
from hs_coo_codes.columns import header_map, InventoryColumns
from hs_coo_codes.upload_to_shopify import Codes

GRAPHQL_URL = "https://test-store.myshopify.com/admin/api/2026-10/graphql.json"
HEADER = [header_map[column][0] for column in InventoryColumns]
TSHIRT_CODES = Codes("JP", "610910", "6109100012")
JEANS_CODES = Codes("JP", "620342", "6203424011")


def make_row(sku: str, codes: Codes) -> list[str]:
    """Create a valid CSV row with the given SKU and codes"""
    row = [""] * len(InventoryColumns)
    row[InventoryColumns.HANDLE] = "handle"
    row[InventoryColumns.TITLE] = "Title"
    row[InventoryColumns.OPTION1_NAME] = "Size"
    row[InventoryColumns.OPTION1_VALUE] = "M"
    row[InventoryColumns.SKU] = sku
    row[InventoryColumns.HS_CODE] = codes.hs
    row[InventoryColumns.COO] = codes.coo
    row[InventoryColumns.LOCATION] = "Hamburg Store IH Germany"
    for column in (InventoryColumns.INCOMING, InventoryColumns.UNAVAILABLE,
                   InventoryColumns.COMMITTED, InventoryColumns.AVAILABLE,
                   InventoryColumns.ON_HAND_CURRENT):
        row[column] = "0"
    row[InventoryColumns.US_HTS_CODE] = codes.us_hts
    return row


class FakeResponse:
    """A requests.Response that returns a fixed result"""
    def __init__(self, result=None, http_error=False, bad_json=False):
        self.result = result
        self.http_error = http_error
        self.bad_json = bad_json

    def raise_for_status(self):
        """Raise an HTTPError if this response is an HTTP error"""
        if self.http_error:
            raise requests.HTTPError("401 Client Error: Unauthorized")

    def json(self):
        """Return the result, or raise ValueError for invalid JSON"""
        if self.bad_json:
            raise ValueError("Expecting value")
        return self.result


class FakeSession:
    """A requests.Session that returns the given responses in order"""
    def __init__(self, *responses):
        self.responses = list(responses)
        self.posts = []

    def post(self, url, json, timeout):
        """Record the request and return the next response"""
        self.posts.append((url, json, timeout))
        return self.responses.pop(0)


def ok_result(data, available=2000):
    """A successful GraphQL result with the given remaining budget"""
    return {"data": data, "extensions": {"cost": {"requestedQueryCost": 10, "throttleStatus": {
        "maximumAvailable": 2000.0, "currentlyAvailable": available, "restoreRate": 100.0}}}}


def throttled_result(requested=300, available=100):
    """A GraphQL result rejected because of throttling"""
    return {"errors": [{"message": "Throttled", "extensions": {"code": "THROTTLED"}}],
            "extensions": {"cost": {"requestedQueryCost": requested, "throttleStatus": {
                "maximumAvailable": 2000.0, "currentlyAvailable": available,
                "restoreRate": 100.0}}}}


@pytest.fixture(name="sleeps")
def fixture_sleeps(monkeypatch):
    """Replace time.sleep and record the sleep durations"""
    durations = []
    monkeypatch.setattr(upload_to_shopify.time, "sleep", durations.append)
    return durations


# _get_csv_sku_to_codes

def test_csv_sku_to_codes_valid():
    """Rows for the same SKU are merged and rows without an SKU are skipped"""
    rows = [make_row("IHT-1610-WHT", TSHIRT_CODES),
            make_row("IHT-1610-WHT", TSHIRT_CODES),
            make_row("IH-634S", JEANS_CODES),
            make_row("", JEANS_CODES)]
    assert upload_to_shopify._get_csv_sku_to_codes(iter(rows), len(HEADER)) == {
        "IHT-1610-WHT": TSHIRT_CODES, "IH-634S": JEANS_CODES}


def test_csv_sku_to_codes_logs_rows_without_sku(caplog):
    """Rows without an SKU are counted in a warning"""
    rows = [make_row("", TSHIRT_CODES), make_row("", JEANS_CODES)]
    assert upload_to_shopify._get_csv_sku_to_codes(iter(rows), len(HEADER)) == {}
    assert "2 rows do not have an SKU" in caplog.text


@pytest.mark.parametrize("codes", [
    Codes("XX", "610910", "6109100012"),
    Codes("JP", "610910", "610910001"),
    Codes("JP", "610910", "61091000１2"),
    Codes("JP", "610910", "610910001A"),
    Codes("JP", "620342", "6109100012"),
], ids=["invalid coo", "short us hts", "non-ascii us hts", "non-digit us hts",
        "hs not prefix of us hts"])
def test_csv_sku_to_codes_invalid_codes(codes):
    """Invalid codes in a row return None"""
    rows = [make_row("IHT-1610-WHT", codes)]
    assert upload_to_shopify._get_csv_sku_to_codes(iter(rows), len(HEADER)) is None


@pytest.mark.parametrize("codes", [
    Codes("CN", "610910", "6109100012"),
    Codes("JP", "610990", "6109901060"),
    Codes("JP", "610910", "6109100004"),
], ids=["different coo", "different hs", "different us hts"])
def test_csv_sku_to_codes_inconsistent_codes(codes):
    """Different codes for the same SKU return None"""
    rows = [make_row("IHT-1610-WHT", TSHIRT_CODES), make_row("IHT-1610-WHT", codes)]
    assert upload_to_shopify._get_csv_sku_to_codes(iter(rows), len(HEADER)) is None


def test_csv_sku_to_codes_invalid_row():
    """A row that fails validation returns None"""
    row = make_row("IHT-1610-WHT", TSHIRT_CODES)
    row[InventoryColumns.LOCATION] = ""
    assert upload_to_shopify._get_csv_sku_to_codes(iter([row]), len(HEADER)) is None


# _create_session

@pytest.fixture(name="shopify_env")
def fixture_shopify_env(monkeypatch):
    """Set the Shopify environment variables"""
    monkeypatch.setenv("SHOPIFY_STORE", "test-store.myshopify.com")
    monkeypatch.setenv("SHOPIFY_CLIENT_ID", "client-id")
    monkeypatch.setenv("SHOPIFY_CLIENT_SECRET", "client-secret")


def test_create_session(shopify_env, monkeypatch):  # pylint: disable=unused-argument
    """A token is requested with the client credentials and set on the session"""
    requests_made = []

    def fake_post(url, timeout, data):
        requests_made.append((url, data))
        return FakeResponse({"access_token": "token"})

    monkeypatch.setattr(upload_to_shopify.requests, "post", fake_post)
    session, graphql_url = upload_to_shopify._create_session()
    assert session.headers["X-Shopify-Access-Token"] == "token"
    assert graphql_url == GRAPHQL_URL
    assert requests_made == [("https://test-store.myshopify.com/admin/oauth/access_token",
                              {"grant_type": "client_credentials", "client_id": "client-id",
                               "client_secret": "client-secret"})]


@pytest.mark.parametrize("variable", ["SHOPIFY_STORE", "SHOPIFY_CLIENT_ID",
                                      "SHOPIFY_CLIENT_SECRET"])
def test_create_session_missing_variable(shopify_env, monkeypatch, variable):  # pylint: disable=unused-argument
    """A missing environment variable returns None without a request"""
    monkeypatch.delenv(variable)
    monkeypatch.setattr(upload_to_shopify.requests, "post",
                        lambda *args, **kwargs: pytest.fail("unexpected request"))
    assert upload_to_shopify._create_session() is None


@pytest.mark.parametrize("response", [
    FakeResponse(http_error=True),
    FakeResponse(bad_json=True),
    FakeResponse({"error": "invalid_client"}),
], ids=["http error", "invalid json", "no access token"])
def test_create_session_failure(shopify_env, monkeypatch, response):  # pylint: disable=unused-argument
    """A failed token request returns None"""
    monkeypatch.setattr(upload_to_shopify.requests, "post", lambda *args, **kwargs: response)
    assert upload_to_shopify._create_session() is None


def test_create_session_connection_error(shopify_env, monkeypatch):  # pylint: disable=unused-argument
    """A connection error returns None"""
    def fake_post(*args, **kwargs):
        raise requests.ConnectionError("no network")

    monkeypatch.setattr(upload_to_shopify.requests, "post", fake_post)
    assert upload_to_shopify._create_session() is None


# _graphql

def test_graphql_returns_data(sleeps):
    """A successful query returns its data without sleeping"""
    session = FakeSession(FakeResponse(ok_result({"shop": {"name": "Test"}})))
    assert upload_to_shopify._graphql(session, GRAPHQL_URL, "query", {"a": 1}) == {
        "shop": {"name": "Test"}}
    assert session.posts == [(GRAPHQL_URL, {"query": "query", "variables": {"a": 1}}, 60)]
    assert not sleeps


@pytest.mark.parametrize("response", [
    FakeResponse(http_error=True),
    FakeResponse(bad_json=True),
    FakeResponse({"errors": [{"message": "Field 'x' doesn't exist"}]}),
], ids=["http error", "invalid json", "graphql error"])
def test_graphql_failure(sleeps, response):
    """A failed query returns None without retrying"""
    session = FakeSession(response)
    assert upload_to_shopify._graphql(session, GRAPHQL_URL, "query", {}) is None
    assert len(session.posts) == 1
    assert not sleeps


def test_graphql_low_budget_sleeps(sleeps, caplog):
    """A low remaining budget sleeps until the budget is half full"""
    caplog.set_level(logging.INFO)
    session = FakeSession(FakeResponse(ok_result({"x": 1}, available=300)))
    assert upload_to_shopify._graphql(session, GRAPHQL_URL, "query", {}) == {"x": 1}
    assert sleeps == [7.0]
    assert "budget low" in caplog.text


def test_graphql_throttled_then_success(sleeps, caplog):
    """A throttled query waits for the requested cost and is retried"""
    session = FakeSession(FakeResponse(throttled_result(requested=300, available=100)),
                          FakeResponse(ok_result({"x": 1})))
    assert upload_to_shopify._graphql(session, GRAPHQL_URL, "query", {}) == {"x": 1}
    assert len(session.posts) == 2
    assert sleeps == [3.0]
    assert "throttled" in caplog.text


def test_graphql_throttled_too_often(sleeps):
    """A query throttled on every attempt returns None after the maximum retries"""
    retries = upload_to_shopify.MAX_THROTTLE_RETRIES
    session = FakeSession(*[FakeResponse(throttled_result()) for _ in range(retries + 1)])
    assert upload_to_shopify._graphql(session, GRAPHQL_URL, "query", {}) is None
    assert len(session.posts) == retries + 1
    assert len(sleeps) == retries


def test_graphql_throttled_without_cost(sleeps):
    """A throttled query without cost information is not retried"""
    result = throttled_result()
    del result["extensions"]
    session = FakeSession(FakeResponse(result))
    assert upload_to_shopify._graphql(session, GRAPHQL_URL, "query", {}) is None
    assert len(session.posts) == 1
    assert not sleeps


# _get_shopify_sku_to_items

def make_variant(sku, item_id, coo="JP", hs=None, country_codes=(), more_country_codes=False):
    """Create a variant node as returned by the variants query"""
    return {"sku": sku, "inventoryItem": {
        "id": item_id, "countryCodeOfOrigin": coo, "harmonizedSystemCode": hs,
        "countryHarmonizedSystemCodes": {
            "pageInfo": {"hasNextPage": more_country_codes},
            "nodes": [{"countryCode": country, "harmonizedSystemCode": code}
                      for country, code in country_codes]}}}


def make_page(variants, end_cursor=None):
    """Create a page of the variants query"""
    return {"productVariants": {
        "pageInfo": {"hasNextPage": end_cursor is not None, "endCursor": end_cursor},
        "nodes": variants}}


def patch_graphql(monkeypatch, *pages):
    """Replace _graphql with one returning the given pages, and record the variables"""
    calls = []
    remaining = list(pages)

    def fake_graphql(session, graphql_url, query, variables):
        calls.append(dict(variables))
        return remaining.pop(0)

    monkeypatch.setattr(upload_to_shopify, "_graphql", fake_graphql)
    return calls


def test_shopify_sku_to_items_pages(monkeypatch):
    """All pages are read, passing the cursor of each page to the next"""
    calls = patch_graphql(
        monkeypatch,
        make_page([make_variant("IHT-1610-WHT", "gid/1", hs="610910",
                                country_codes=[("CA", "6109100000"), ("US", "6109100012")])],
                  end_cursor="cursor1"),
        make_page([make_variant("IHT-1610-WHT", "gid/2"),
                   make_variant("IH-634S", "gid/3", country_codes=[("CA", "6203420000")])]))
    assert upload_to_shopify._get_shopify_sku_to_items(None, GRAPHQL_URL) == {
        "IHT-1610-WHT": [("gid/1", Codes("JP", "610910", "6109100012")),
                         ("gid/2", Codes("JP", None, None))],
        "IH-634S": [("gid/3", Codes("JP", None, None))]}
    assert [call["cursor"] for call in calls] == [None, "cursor1"]


def test_shopify_sku_to_items_skips_variants_without_sku(monkeypatch, caplog):
    """Variants without an SKU are skipped and counted in a warning"""
    patch_graphql(monkeypatch, make_page([make_variant(None, "gid/1"),
                                          make_variant("", "gid/2"),
                                          make_variant("IH-634S", "gid/3")]))
    assert upload_to_shopify._get_shopify_sku_to_items(None, GRAPHQL_URL) == {
        "IH-634S": [("gid/3", Codes("JP", None, None))]}
    assert "2 variants do not have an SKU" in caplog.text


def test_shopify_sku_to_items_too_many_country_codes(monkeypatch):
    """An item with more country codes than were read returns None"""
    patch_graphql(monkeypatch, make_page([make_variant("IH-634S", "gid/1",
                                                       more_country_codes=True)]))
    assert upload_to_shopify._get_shopify_sku_to_items(None, GRAPHQL_URL) is None


def test_shopify_sku_to_items_query_failure(monkeypatch):
    """A failed query on a later page returns None instead of partial results"""
    patch_graphql(monkeypatch, make_page([make_variant("IH-634S", "gid/1")], end_cursor="c1"),
                  None)
    assert upload_to_shopify._get_shopify_sku_to_items(None, GRAPHQL_URL) is None


# _create_id_to_codes

def test_create_id_to_codes():
    """Only items whose codes differ from the CSV are uploaded, with the CSV codes"""
    csv_sku_to_codes = {"IHT-1610-WHT": TSHIRT_CODES, "IH-634S": JEANS_CODES}
    shopify_sku_to_items = {
        "IHT-1610-WHT": [("gid/1", TSHIRT_CODES), ("gid/2", Codes("JP", None, None))],
        "IH-634S": [("gid/3", JEANS_CODES)],
        "IH-ONLY-IN-SHOPIFY": [("gid/4", Codes(None, None, None))]}
    id_to_codes, skipped_skus = upload_to_shopify._create_id_to_codes(csv_sku_to_codes,
                                                                     shopify_sku_to_items)
    assert id_to_codes == {"gid/2": TSHIRT_CODES}
    assert not skipped_skus


def test_create_id_to_codes_sku_not_in_shopify():
    """SKUs in the CSV but not in Shopify are returned as skipped"""
    id_to_codes, skipped_skus = upload_to_shopify._create_id_to_codes(
        {"IH-634S": JEANS_CODES, "IH-MISSING": TSHIRT_CODES},
        {"IH-634S": [("gid/3", Codes("JP", None, None))]})
    assert id_to_codes == {"gid/3": JEANS_CODES}
    assert skipped_skus == ["IH-MISSING"]


def test_create_id_to_codes_already_synced(caplog):
    """Nothing is uploaded when Shopify already matches the CSV"""
    caplog.set_level(logging.INFO)
    id_to_codes, skipped_skus = upload_to_shopify._create_id_to_codes(
        {"IH-634S": JEANS_CODES}, {"IH-634S": [("gid/3", JEANS_CODES)]})
    assert id_to_codes == {}
    assert not skipped_skus
    assert "already synced" in caplog.text


# upload_to_shopify

def write_csv(path, rows, header=None):
    """Write an inventory CSV to path"""
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER if header is None else header)
        writer.writerows(rows)


@pytest.fixture(name="uploads")
def fixture_uploads(monkeypatch):
    """Mock the Shopify API calls of upload_to_shopify and record the uploads"""
    uploaded = []
    monkeypatch.setattr(upload_to_shopify, "_create_session", lambda: ("session", GRAPHQL_URL))
    monkeypatch.setattr(upload_to_shopify, "_get_shopify_sku_to_items", lambda session, url: {
        "IHT-1610-WHT": [("gid/1", TSHIRT_CODES), ("gid/2", Codes("JP", None, None))]})

    def fake_upload(session, graphql_url, id_to_codes):
        uploaded.append(id_to_codes)
        return True

    monkeypatch.setattr(upload_to_shopify, "_upload_codes_to_shopify", fake_upload)
    return uploaded


def test_upload_to_shopify(tmp_path, uploads):
    """Changed items are passed to the upload"""
    input_file = tmp_path / "input.csv"
    write_csv(input_file, [make_row("IHT-1610-WHT", TSHIRT_CODES)])
    assert upload_to_shopify.upload_to_shopify(str(input_file))
    assert uploads == [{"gid/2": TSHIRT_CODES}]


def test_upload_to_shopify_sku_not_in_shopify(tmp_path, uploads):
    """A CSV SKU missing from Shopify fails before anything is uploaded"""
    input_file = tmp_path / "input.csv"
    write_csv(input_file, [make_row("IHT-1610-WHT", TSHIRT_CODES),
                           make_row("IH-MISSING", JEANS_CODES)])
    assert not upload_to_shopify.upload_to_shopify(str(input_file))
    assert not uploads


def test_upload_to_shopify_without_us_hts_column(tmp_path, uploads):
    """A CSV without the US HTS column fails before anything is uploaded"""
    input_file = tmp_path / "input.csv"
    write_csv(input_file, [make_row("IHT-1610-WHT", TSHIRT_CODES)[:-1]], header=HEADER[:-1])
    assert not upload_to_shopify.upload_to_shopify(str(input_file))
    assert not uploads


def test_upload_to_shopify_empty_file(tmp_path, uploads):
    """An empty file fails"""
    input_file = tmp_path / "input.csv"
    input_file.write_text("", encoding="utf-8")
    assert not upload_to_shopify.upload_to_shopify(str(input_file))
    assert not uploads


def test_upload_to_shopify_session_failure(tmp_path, uploads, monkeypatch):
    """A failure to connect to Shopify fails before anything is uploaded"""
    monkeypatch.setattr(upload_to_shopify, "_create_session", lambda: None)
    input_file = tmp_path / "input.csv"
    write_csv(input_file, [make_row("IHT-1610-WHT", TSHIRT_CODES)])
    assert not upload_to_shopify.upload_to_shopify(str(input_file))
    assert not uploads
