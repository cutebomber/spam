"""
TON Ad Campaign Script
Sends 0.001 TON with a custom ad memo to a list of addresses.

Requirements:
    pip install tonsdk requests

Usage:
    1. Fill in your mnemonic phrase, ad text, and target addresses below
    2. Run: python ton_ad_campaign.py
"""

import time
import asyncio
from tonsdk.contract.wallet import WalletVersionEnum, Wallets
from tonsdk.utils import to_nano, bytes_to_b64str
from tonsdk.crypto import mnemonic_to_wallet_key
import requests

# ─────────────────────────────────────────────
#  CONFIG — edit these before running
# ─────────────────────────────────────────────

MNEMONIC = "key soldier fossil such naive grab else property ethics retire enact advice scissors hen inflict brand quick monkey toss plunge canal garage dress gasp"

AD_TEXT = """🔥 @ikycbot — Fragment verified accounts
⚡ Fully automated
💸 $5 per account
🚀 Instant delivery
Grab yours now!"""

AMOUNT_TON = 0.001          # TON per address
DELAY_SECONDS = 2           # Pause between sends (avoid rate limits)

# List of target TON wallet addresses
TARGET_ADDRESSES = [
    """UQDfj1w3Hn6VY82bvXZFlGeozPe1tLQqYyThONIQD6vuJ0mv
UQAYOSUmqovB-1tk7AZvuwUXiCkxa7jfDCbl1Mb4HXA6uDhU
UQD3CH6-Y-9KivftQsCJH-wj13-bKVPYHILvxllOzXJbSprj
UQAPWAu-xv0LQalpNZAnF98G8DKQYl_Eoo4VG03ogdjPdb8T
UQD6-VOldDRmUFIxqsVVJ19rTa2SMNVGo24-dnw1oBMYH0T4
UQCuWRdU_BL2xk1l-ooW3kvB4xxxDOACwmiCQsXdLxIphHzL
UQB5xf0k0msKiZ2zRgNuylAlcDTuMJDYV3V49mdxbaiDLhUC
UQA_Bgca2Bmnm_1zs6VAI_Zl2DiDdPJQOSpNm6pjqSqlpkWL
UQDq1cCNORhQSqgZJt4sEBbZJjYekJ_R1ZD21_vo2WwZaZDb
UQBRntQA77dPqDdYmOabN2DCZuopIkluDAIlaCYI1gitAbEu
UQAxgOa13dB7S2ms17121UFn8xj36psxE7B8qSlgSg8mCTBh
UQBpq0Ni7v0BQiaQTq1C8C-BA6S-JvQH0RS7urMJYuV3AM4e
UQADMgN3y9ateSDtwPf9FnonwN1fNzghsglU9ALsUM6oPD6j
UQDFPTIyFD3ONyTee8NMLWBrAkzb9PMLTVEBdi4O20du_nC-
UQDSbjfIoalHHea1GSGpd0RF81-51LLBP0Dc3Ed5e-aR5tHX
UQAnnQyWy93mnoO_-sBxOlQthxujFbEhekhKOQH3KclZOla7
EQA51jCD5I9GRS_4oEzQ03M6kMi-KZqllRtidBdZssF-DjDh
UQDeWRr9wKlB_0zs1JktwWw-v-mBgeHncOpUM_ZVZavC0Zjp
UQDjDFBC-ULpF5W9DnYdTwWl3cHbSsUp3W3NxdpC_e0sEMw0
UQDD6ud_dK5yoEouCtIt9MTWdN05TFfLjxk-wdviJytTPG7F
UQBj2p6CqbP5kNH7EUf10aJMnsYg3KztLZX1ftn7_V-h3tLn
UQBqEBYtcp1zw8Lj7ddVYXzOLUP1qiFdsNAzXtOWQ2-8nOdZ
UQAkaJocDfkuh36R3Km5s0T1xVEODDY1DuWYWNlPkNsF22At
UQADpHxkI2_VjlzymDT-GbPCMzyjNwiItxcZ0c9kcgStsY4f
UQA1QRy1Lh3BYPWV1Jc7C3dai4cjw04KXsldoX5i3vl2X0Xe
UQA_aXWcT61qDiOYGldaU5j80pF0stc8fx37I3R2qgmNON2x
EQAG3l0Nqby8z2g7KsHLidxA_9kR2-ZyDQZEk5u3r0L7yY0x
EQAiU6mdsMdBDTCOPQm_n_xM5DpK4DZtYwi1CHAWtOsKLKrA
EQB653-R3QP0GSf87vMD09idkQIynQh27PtOtAlu1aUPZ9w0
EQB0Djdq_2kfGBaw498Jr6XXIygW0i7H1vOEvNit7ixXwSkf
EQARg_NjjtuxOrglyKy21MwLAb3hu85SvkLWtNnF-jVP9WVo
EQDSkS_0GAJK30Q3jHZHAHqTb11YsdZkpF513N100NBgPfcK
UQCovbebCEekTKVoFWcbI9rCphs1mRLP6A8pYXz2DMFNrIc8
UQBGfCnOZkUGWL8k1tOi7w6Bkg4rOyT3chDdQQZP47dtWGkG
UQAYxdiXrXgnHyFvOjENU5LEpncPn8t1PjnfkwXpafjCAlsC
UQAhZiSt9QaHXhFK_5aOD69_8zS7hu6jSKqJ9ETq5vIWygnL
UQBx8q5-M9FFNcQ2lTr3GSas1v66Y9k4zsFLEJF63MjCNlfD
UQBQWpJBkDc7QBM3Z75bq070qhZ62AhxQqYfLFV2R1XR8h0_
UQBeC7mSrLKYooizly4m7fQbSRm4qCMO7Pg9_Kt5HiQOh2So
UQCmkyHN4QPMiWSzZGT6Af4T6vyFLqWV5odlCsIwL532YxbV
UQDFgZ0ujlNuofOhW8kYvfROeP4fHHZkvIpYKPvtV6zKRAf1"""
    # Add more addresses here...
]

# TON API endpoint (mainnet)
TON_API_URL = "https://toncenter.com/api/v2"
TON_API_KEY = "640b4486094ffd81a5e49a4bb7c599fb55e8bfa3d391f140fb02b12b10c032ca"  # Optional: get free key at https://t.me/tonapibot for higher rate limits

# ─────────────────────────────────────────────
#  CORE FUNCTIONS
# ─────────────────────────────────────────────

def get_wallet(mnemonic_phrase: str):
    """Derive wallet keys and contract from mnemonic."""
    mnemonics = mnemonic_phrase.strip().split()
    if len(mnemonics) not in (12, 24):
        raise ValueError(f"Expected 12 or 24 mnemonic words, got {len(mnemonics)}")
    
    pub_key, priv_key = mnemonic_to_wallet_key(mnemonics)
    wallet = Wallets.create(WalletVersionEnum.v4r2, pub_key=pub_key, private_key=priv_key, wc=0)
    return wallet, pub_key, priv_key, mnemonics


def get_seqno(address: str) -> int:
    """Fetch current seqno from TON API."""
    params = {"address": address}
    headers = {"X-API-Key": TON_API_KEY} if TON_API_KEY else {}
    
    resp = requests.get(f"{TON_API_URL}/getExtendedAddressInformation",
                        params=params, headers=headers, timeout=15)
    data = resp.json()
    
    if not data.get("ok"):
        raise RuntimeError(f"API error fetching seqno: {data}")
    
    result = data["result"]
    # If wallet not yet deployed, seqno = 0
    account_state = result.get("account_state", {})
    if account_state.get("wallet_type") is None:
        return 0
    
    return result.get("seqno", 0)


def send_boc(boc_b64: str) -> dict:
    """Broadcast a signed BOC to the network."""
    headers = {"X-API-Key": TON_API_KEY} if TON_API_KEY else {}
    resp = requests.post(
        f"{TON_API_URL}/sendBoc",
        json={"boc": boc_b64},
        headers=headers,
        timeout=15
    )
    return resp.json()


def build_transfer(wallet, priv_key, seqno: int, to_address: str, amount_ton: float, memo: str):
    """Build and sign a transfer message."""
    query = wallet.create_transfer_message(
        to_addr=to_address,
        amount=to_nano(amount_ton, "ton"),
        seqno=seqno,
        payload=memo,
    )
    return bytes_to_b64str(query["message"].to_boc(False))


# ─────────────────────────────────────────────
#  MAIN CAMPAIGN RUNNER
# ─────────────────────────────────────────────

def run_campaign():
    print("=" * 55)
    print("  TON Ad Campaign Script")
    print("=" * 55)

    # Load wallet
    print("\n[1/3] Loading wallet from mnemonic...")
    wallet, pub_key, priv_key, mnemonics = get_wallet(MNEMONIC)
    wallet_address = wallet.address.to_string(True, True, True)
    print(f"  Wallet address : {wallet_address}")

    # Fetch seqno
    print("\n[2/3] Fetching wallet seqno...")
    seqno = get_seqno(wallet_address)
    print(f"  Current seqno  : {seqno}")

    total = len(TARGET_ADDRESSES)
    print(f"\n[3/3] Sending to {total} addresses...")
    print(f"  Amount : {AMOUNT_TON} TON each")
    print(f"  Memo   : {AD_TEXT[:60]}{'...' if len(AD_TEXT) > 60 else ''}")
    print("-" * 55)

    success, failed = 0, 0
    errors = []

    for i, address in enumerate(TARGET_ADDRESSES, 1):
        address = address.strip()
        if not address:
            continue

        print(f"[{i}/{total}] → {address[:20]}...", end=" ", flush=True)

        try:
            boc = build_transfer(wallet, priv_key, seqno, address, AMOUNT_TON, AD_TEXT)
            result = send_boc(boc)

            if result.get("ok"):
                print("✅ sent")
                success += 1
                seqno += 1  # Increment locally for next tx
            else:
                msg = result.get("error", "unknown error")
                print(f"❌ failed — {msg}")
                failed += 1
                errors.append((address, msg))

        except Exception as e:
            print(f"❌ exception — {e}")
            failed += 1
            errors.append((address, str(e)))

        if i < total:
            time.sleep(DELAY_SECONDS)

    # Summary
    print("\n" + "=" * 55)
    print(f"  Campaign complete!")
    print(f"  ✅ Successful : {success}")
    print(f"  ❌ Failed     : {failed}")
    total_spent = success * AMOUNT_TON
    print(f"  💎 Total sent : {total_spent:.4f} TON")
    if errors:
        print("\n  Failed addresses:")
        for addr, err in errors:
            print(f"    {addr[:24]}... → {err}")
    print("=" * 55)


if __name__ == "__main__":
    run_campaign()
