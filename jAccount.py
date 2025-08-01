import base64
import json
import logging
import os
import re
import time
from io import BytesIO
from typing import TypedDict, Dict, Tuple

import cv2
import numpy as np
import requests
from urllib.parse import urlparse, parse_qs
import Files

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

ACADEMIC_INFORMATION_SERVICES_LOGIN_URL = 'https://i.sjtu.edu.cn/jaccountlogin'
ACADEMIC_INFORMATION_SERVICES_LOGOUT_URL = 'https://i.sjtu.edu.cn/logout'
ACADEMIC_INFORMATION_SERVICES_MAIN_PAGE = 'https://i.sjtu.edu.cn/xtgl/index_initMenu.html'
CAPTCHA_FETCH_URL = 'https://jaccount.sjtu.edu.cn/jaccount/captcha'
CAPTCHA_RECOGNIZE_URL = "https://geek.sjtu.edu.cn/captcha-solver/"
LOGIN_ATTEMPTS = 5
JACCOUNT_LOGIN_URL = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin'
JACCOUNT_ACCOUNT = Files.read_config("jAccount", "jAccount")
JACCOUNT_PASSWORD = Files.read_config("jAccount", "Password")


class AuthCookies(TypedDict):
    keepalive: str
    jSessionID: str
    SLSessionID: str


def _auth_cookies_to_dict(auth_cookies: AuthCookies) -> Dict[str, str]:
    """
    Converts the AuthCookies TypedDict into a dictionary suitable for
    the `requests` library cookie jar.

    Args:
        auth_cookies: The AuthCookies object.

    Returns:
        A dictionary with cookie names mapped to their values.
    """
    return {
        'keepalive': auth_cookies['keepalive'],
        'JSESSIONID': auth_cookies['jSessionID'],
        'sl-session': auth_cookies['SLSessionID']
    }


def _recognize_captcha(session: requests.Session, image_bytes: bytes) -> str:
    """
    Sends the captcha image bytes to an external recognition service.

    Args:
        session: The requests session to use for the request.
        image_bytes: The captcha image in bytes format.

    Returns:
        The recognized captcha text.

    Raises:
        RuntimeError: If the captcha recognition service fails or returns an error.
    """
    try:
        logger.info("Sending captcha to recognition service...")
        files = {"image": ("captcha.jpg", image_bytes, "image/jpeg")}
        response = session.post(CAPTCHA_RECOGNIZE_URL, files=files, timeout=10)
        response.raise_for_status()
        response_json = response.json()
        result = response_json.get('result')
        if not result:
            raise RuntimeError(f"Captcha service returned an invalid response: {response_json}")
        logger.info(f"Captcha recognized as: '{result}'")
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during captcha recognition: {e}")
        raise RuntimeError(f"Failed to connect to captcha recognition service: {e}") from e
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error parsing captcha service response: {e}")
        raise RuntimeError(f"Invalid response from captcha service: {e}") from e


def _analyze_jaccount_url(url: str) -> Tuple[str, str, str]:
    """
    Parses the jAccount login URL to extract necessary parameters.

    Args:
        url: The full jAccount login URL with query parameters.

    Returns:
        A tuple containing the 'sid', 'client', and 'se' parameters.
    """
    parsed_url = urlparse(url)
    parameters = parse_qs(parsed_url.query)
    return parameters['sid'][0], parameters['client'][0], parameters['se'][0]


def _fetch_and_solve_captcha(session: requests.Session, uuid: str, referer_url: str) -> str:
    """
    Fetches a captcha image, processes it, and gets it recognized.

    Args:
        session: The requests session, which contains the necessary cookies.
        uuid: The UUID associated with the login session.
        referer_url: The URL of the login page to use as the Referer header.

    Returns:
        The recognized captcha text.

    Raises:
        RuntimeError: If fetching or processing the captcha fails.
    """
    try:
        logger.info("Fetching new captcha...")
        params = {"uuid": uuid, "t": int(time.time() * 1000)}
        headers = {"Referer": referer_url}
        response = session.get(CAPTCHA_FETCH_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        image_array = np.frombuffer(response.content, dtype=np.uint8)
        img_data = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        binary = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 2)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morph = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        success, encoded_image = cv2.imencode('.jpg', morph)
        if not success:
            raise RuntimeError("Failed to encode processed captcha image.")

        return _recognize_captcha(session, encoded_image.tobytes())

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch captcha image: {e}")
        raise RuntimeError(f"Failed to fetch captcha: {e}") from e
#
#
# def base64_to_image(base64_str):
#     base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
#     byte_data = base64.b64decode(base64_data)
#     return Image.open(BytesIO(byte_data))
#
#
# def captcha_recognize() -> str:
#     try:
#         result = requests.post(CAPTCHA_RECOGNIZE_URL, files={"image": open('captcha.jpg', 'rb')}).json()['result']
#         return result
#     except Exception as e:
#         raise RuntimeError(Files.exception_throw_out()) from e
#
#
# def captcha(uuid: str = "", header=None, cookie=None) -> str:
#     if header is None:
#         header = {}
#     if not cookie:
#         cookie = {}
#     params = {
#         "uuid": uuid,
#         "t": int(time.time() * 1000)
#     }
#     response = requests.get(CAPTCHA_FETCH_URL, params=params, headers=header, cookies=cookie)
#     response.raise_for_status()
#     image_array = np.frombuffer(response.content, dtype=np.uint8)
#     img_data = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
#     gray = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (3, 3), 0)
#     binary = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 2)
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
#     morph = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
#     cv2.imwrite('captcha.jpg', morph)
#     result = captcha_recognize()
#     os.remove("captcha.jpg")
#     return result


def login(account: str = "", password: str = "") -> AuthCookies:
    """
    Logs into SJTU jAccount and retrieves authentication cookies.

    This function navigates the SJTU single sign-on process, handles captchas,
    and follows redirects to obtain the necessary cookies for accessing
    authenticated services.

    Args:
        account: The jAccount username.
        password: The jAccount password.

    Returns:
        An AuthCookies object containing the 'keepalive', 'jSessionID',
        and 'SLSessionID' cookies.

    Raises:
        LoginError: If login fails after all attempts.
        RuntimeError: If a critical step like fetching the login page fails.
    """
    with requests.Session() as session:
        try:
            logger.info("Accessing the academic information services login page...")
            initial_response = session.get(ACADEMIC_INFORMATION_SERVICES_LOGIN_URL, timeout=10)
            initial_response.raise_for_status()
            login_page_url = initial_response.url
            logger.info(f"Redirected to jAccount login page: {login_page_url}")

            login_params = _analyze_jaccount_url(login_page_url)
            uuid_match = re.search(r'(?<=uuid: ")(.*?)(?=")', initial_response.text)
            if not uuid_match:
                raise RuntimeError("Could not find UUID on the login page.")
            uuid = uuid_match.group(0)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to access the initial login page: {e}") from e
        for attempt in range(LOGIN_ATTEMPTS):
            logger.info(f"Login attempt {attempt + 1}/{LOGIN_ATTEMPTS}...")
            captcha_solution = _fetch_and_solve_captcha(session, uuid, login_page_url)
            data = {
                "sid": login_params[0],
                "client": login_params[1],
                "se": login_params[2],
                "v": "",
                "uuid": uuid,
                "user": account,
                "pass": password,
                "captcha": captcha_solution,
                "lt": "p",
                "returl": "CECx0MIDBcwuRlXc3fEWcd64FwYy0rxvIoRM7ExIOqrLXO1ZbcVPQnqAsOJgXsVihTq+0+hvOiYe"
            }
            try:
                login_response = session.post(JACCOUNT_LOGIN_URL, data=data, headers={"Referer": login_page_url},
                                              timeout=10)
                login_response.raise_for_status()
                login_result = login_response.json()
                if login_result.get("errno") == 0:
                    logger.info("Login credentials accepted. Following redirects to get final cookies.")
                    final_response = session.get(login_page_url, timeout=10)
                    final_response.raise_for_status()
                    jSessionID=""
                    for cookie in final_response.cookies:
                        if cookie.name == "JSESSIONID" and cookie.domain=="i.sjtu.edu.cn/":
                            jSessionID = cookie.value
                            break
                    for resp in final_response.history:
                        if 'keepalive' in resp.cookies:
                            return AuthCookies(
                                keepalive=resp.cookies['keepalive'],
                                jSessionID=jSessionID,
                                SLSessionID=session.cookies['sl-session'],
                            )
                        if 'keepalive' in final_response.cookies and 'sl-session' in final_response.cookies:
                            return AuthCookies(
                                keepalive=resp.cookies['keepalive'],
                                jSessionID=jSessionID,
                                SLSessionID=session.cookies['sl-session'],
                            )
                else:
                    error_message = login_result.get("error", "Unknown error")
                    logger.warning(f"Login attempt failed: {error_message}")
                    time.sleep(1)
            except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                logger.error(f"An error occurred during login attempt: {e}")
                time.sleep(1)
    raise RuntimeError(f"Login failed after {LOGIN_ATTEMPTS} attempts.")


def logout(user_auth_cookies: AuthCookies) -> None:
    """
    Logs out from the academic information services.

    Args:
        user_auth_cookies: The authentication cookies for the session to be terminated.
    """
    if not user_auth_cookies:
        logger.warning("Logout called with no cookies provided. Skipping.")
        return

    logger.info("Logging out...")
    cookies = _auth_cookies_to_dict(user_auth_cookies)
    try:
        response = requests.get(ACADEMIC_INFORMATION_SERVICES_LOGOUT_URL, cookies=cookies, timeout=10)
        response.raise_for_status()
        logger.info("Successfully logged out.")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred during logout: {e}")


def is_login(user_auth_cookies: AuthCookies) -> bool:
    """
    Checks if the provided cookies correspond to an active login session.

    Args:
        user_auth_cookies: The authentication cookies to verify.

    Returns:
        True if the session is active, False otherwise.
    """
    if not user_auth_cookies or not all(user_auth_cookies.values()):
        return False

    cookies = _auth_cookies_to_dict(user_auth_cookies)
    try:
        response = requests.get(ACADEMIC_INFORMATION_SERVICES_MAIN_PAGE, cookies=cookies, allow_redirects=False,
                                timeout=10)
        response.raise_for_status()
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while checking login status: {e}")
        return False


def test_login_flow():
    """
    Executes a full test of the login and logout functionality.

    This test will:
    1. Attempt to log in with the configured credentials.
    2. Assert that the login was successful.
    3. Verify the login status.
    4. Log out from the session.
    5. Assert that the logout was successful by re-verifying status.
    """
    logger.info("--- Starting jAccount Login Test ---")

    auth_cookies = None
    try:
        logger.info(f"Step 1: Attempting to log in as '{JACCOUNT_ACCOUNT}'...")
        auth_cookies = login(JACCOUNT_ACCOUNT, JACCOUNT_PASSWORD)
        assert auth_cookies and all(auth_cookies.values())
        logger.info("Step 1 PASSED: Login successful, received auth cookies.")
        logger.info("Step 2: Verifying login status...")
        status = is_login(auth_cookies)
        assert status is True
        logger.info("Step 2 PASSED: Login status confirmed as 'Logged In'.")
    except (RuntimeError, requests.exceptions.RequestException) as e:
        logger.error(f"Test FAILED during login/verification phase: {e}")
    except AssertionError:
        logger.error("Test FAILED: Assertion failed during login/verification.")
    finally:
        if auth_cookies:
            logger.info("Step 3: Attempting to log out...")
            logout(auth_cookies)

            # 4. Verify Logout
            logger.info("Step 4: Verifying logout status...")
            status_after_logout = is_login(auth_cookies)
            try:
                assert status_after_logout is False
                logger.info("Step 4 PASSED: Logout status confirmed as 'Logged Out'.")
                logger.info("--- jAccount Login Test Completed Successfully ---")
            except AssertionError:
                logger.error("Test FAILED: User is still logged in after logout attempt.")


if __name__ == '__main__':
    test_login_flow()

