from flask import Flask, render_template, request
from datetime import datetime, timedelta
import os

# Tell Flask where to find templates and static files
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

@app.route("/", methods=["GET", "POST"])
def planner():
    if request.method == "POST":
        # 1️⃣ Get form data
        wake_time_str = request.form.get("wake_time")  # "HH:MM"
        study_hours = float(request.form.get("study", 0))
        travel_hours = float(request.form.get("travel", 0))
        task = request.form.get("task", "")

        # 2️⃣ Convert wake time to datetime
        wake_time = datetime.strptime(wake_time_str, "%H:%M")

        # 3️⃣ Prepare schedule
        schedule = []

        # Wake up
        schedule.append(f"Wake up at {wake_time.strftime('%H:%M')}")

        # Study period
        study_end = wake_time + timedelta(hours=study_hours)
        schedule.append(f"Study from {wake_time.strftime('%H:%M')} to {study_end.strftime('%H:%M')}")

        # Travel period
        travel_end = study_end + timedelta(hours=travel_hours)
        schedule.append(f"Travel from {study_end.strftime('%H:%M')} to {travel_end.strftime('%H:%M')}")

        # Task period (assume 2 hours)
        task_end = travel_end + timedelta(hours=2)
        schedule.append(f"Do task '{task}' from {travel_end.strftime('%H:%M')} to {task_end.strftime('%H:%M')}")

        # Free time
        total_hours = 24
        sleep_hours = 8
        freetime_hours = total_hours - sleep_hours - study_hours - travel_hours - 2
        if freetime_hours > 0:
            schedule.append(f"Free time for {freetime_hours} hours")

        return render_template(
            "planner.html",
            wake_time=wake_time_str,
            study=study_hours,
            travel=travel_hours,
            task=task,
            freetime=freetime_hours,
            schedule=schedule
        )

    # GET request
    return render_template(
        "planner.html",
        wake_time="07:00",
        study="",
        travel="",
        task="",
        freetime="",
        schedule=None
    )

if __name__ == "__main__":
    # Use Render's dynamic port or default 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
