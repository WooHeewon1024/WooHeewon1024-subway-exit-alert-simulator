"""Flask server for the subway exit-alert simulator.

The server owns the passenger, train, timing, route, and display state.
JavaScript only asks this API for the latest state and draws the interface.
"""
import os
from threading import Lock
from time import monotonic

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

STATIONS = [
    "장암", "도봉산", "수락산", "마들", "노원", "중계", "하계", "공릉", "태릉입구",
    "먹골", "중화", "상봉", "면목", "사가정", "용마산", "중곡", "어린이대공원",
]
TRAVEL_SECONDS = 6  # 실제 60초 이동을 10배 빠르게 시연합니다.
state_lock = Lock()
state = {
    "seat": {"id": 1, "occupied": False, "remaining": 0},
    "train": {"station": 0, "direction": 1, "exited": 0, "running": True, "last_tick": monotonic()},
}


def status_for(seat):
    """Return the text badge and CSS class from Python-managed seat data."""
    if not seat["occupied"]:
        return {"label": "빈 좌석", "class_name": "normal"}
    if seat["remaining"] == 0:
        return {"label": "하차 알림", "class_name": "exit"}
    if seat["remaining"] <= 2:
        return {"label": "하차 임박", "class_name": "urgent"}
    if seat["remaining"] <= 5:
        return {"label": "준비 상태", "class_name": "ready"}
    return {"label": "일반 상태", "class_name": "normal"}


def move_one_station():
    """Move the train once, decrementing the configured passenger count."""
    seat, train = state["seat"], state["train"]
    if seat["occupied"] and seat["remaining"] > 0:
        seat["remaining"] -= 1
    if train["station"] == len(STATIONS) - 1:
        train["direction"] = -1
    elif train["station"] == 0:
        train["direction"] = 1
    train["station"] += train["direction"]


def advance_elapsed_time():
    """Advance all simulation ticks that have elapsed while the train runs."""
    train = state["train"]
    if not train["running"]:
        return
    now = monotonic()
    while now - train["last_tick"] >= TRAVEL_SECONDS:
        move_one_station()
        train["last_tick"] += TRAVEL_SECONDS


def display_message():
    """Build the personal seat notification message on the server."""
    seat, train = state["seat"], state["train"]
    if not seat["occupied"]:
        return "하차 예정 정보를 설정해주세요."
    if seat["remaining"] == 0:
        return "이번 역 하차 알림"
    if seat["remaining"] == 1:
        next_index = train["station"] + train["direction"]
        next_station = STATIONS[next_index] if 0 <= next_index < len(STATIONS) else STATIONS[train["station"]]
        return f"다음 역 하차 예정 · 다음 역 {next_station}"
    return f"하차까지 {seat['remaining']}개 역 남음 · 현재 {STATIONS[train['station']]}역"


def snapshot():
    """Create JSON-safe state for every browser client."""
    seat, train = state["seat"], state["train"]
    return {
        "seat": dict(seat),
        "train": {key: train[key] for key in ("station", "direction", "exited", "running")},
        "stations": STATIONS,
        "status": status_for(seat),
        "display": display_message(),
        "travel_seconds": TRAVEL_SECONDS,
    }


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/state")
def get_state():
    with state_lock:
        advance_elapsed_time()
        return jsonify(snapshot())


@app.post("/api/action")
def update_state():
    data = request.get_json(silent=True) or {}
    action = data.get("action")
    with state_lock:
        advance_elapsed_time()
        seat, train = state["seat"], state["train"]
        if action == "seat":
            command = data.get("command")
            if command == "toggle":
                if not seat["occupied"]:
                    seat["occupied"] = True
                elif seat["remaining"] == 0:
                    seat.update(occupied=False, remaining=0)
                    train["exited"] += 1
                else:
                    seat.update(occupied=False, remaining=0)
            elif command == "plus" and seat["occupied"]:
                seat["remaining"] = min(30, seat["remaining"] + 1)
            elif command == "minus" and seat["occupied"]:
                seat["remaining"] = max(0, seat["remaining"] - 1)
            elif command == "reset" and seat["occupied"]:
                seat["remaining"] = 0
            else:
                return jsonify(error="Unknown seat command"), 400
        elif action == "set-seat":
            try:
                seat["id"] = max(1, min(8, int(data.get("seat_id"))))
            except (TypeError, ValueError):
                return jsonify(error="Seat number must be between 1 and 8"), 400
        elif action == "toggle-running":
            train["running"] = not train["running"]
            train["last_tick"] = monotonic()
        elif action == "restart":
            state["seat"] = {"id": 1, "occupied": False, "remaining": 0}
            state["train"] = {"station": 0, "direction": 1, "exited": 0, "running": True, "last_tick": monotonic()}
        else:
            return jsonify(error="Unknown action"), 400
        return jsonify(snapshot())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
