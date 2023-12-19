from yahoo_automator import YahooAutomator
# winget install --id=Gyan.FFmpeg  -e
# sudo apt install ffmpeg

yahoo_automator = YahooAutomator(profile_dir="./temp_profile",
                                 predefined_cookies="./defaults/startup_cookies.pkl"
                                 )

status = yahoo_automator.login_to_yahoo(
    yahoo_mail="yahoo@yahoo.com",
    passwords_combo=["wrong_pass121", "wrong_pass212", "correctpassword"])

if status[0]:
    print(f"Found password: {yahoo_automator.correct_password}")
else:
    print(status)
    print(yahoo_automator.correct_password)
