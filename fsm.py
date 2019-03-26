import random
from datetime import date, datetime, timedelta
# admn
# readonly
players = [
  {
    "player_name": "huy",
    "quizzes": [{
        'question': 'Học viên đang pick tướng',
        'choices': [0, 0, 0, 2, 0, 0, 0, 0, 0],
        'time_allowed': 12,
        'right_choice_indexes': [3],
        'date_sent': datetime.date(2019, 3, 27),
        'time_sent': datetime.datetime(2019, 3, 27, 0, 44, 28, 400551)
    }],
    "results": [ 
      {
          "correct": True,
          "open_times": 3,
          "rewards": ["Ao phong mindx", "Sex toy"],
      }
    ],
    "extra_quota": 0,
  },
  {
    "player_name": "huy",
    "quizzes": [],
    "results": [],
    "extra_quota": 0,
  },
]

# Hoc: 0
# Facebook: 1
# LOL: 2
# Bug: 3
# Youtube: 4

# admn
# crud
quiz_configs = [
  {
    "questions": [
      "Học viên đang vào fb",
      "Học viên đang lướt facebook",
      "Học viên đang xem newsfeed",
      "Học viên xem face.book"
    ],
    "time_allowed": 12,
    "right_choices_count": 2,
    "wrong_choice_values": [0],
    "right_choice_values": [1]
  },
  {
      "questions": [
          "Học viên đang vào youtube",
          "Học viên đang lướt youtube",
          "Học viên đang xem video",
          "Học viên xem youtube"
      ],
      "time_allowed": 12,
      "right_choices_count": 3,
      "wrong_choice_values": [0],
      "right_choice_values": [4]
  },
  {
      "questions": [
          "Học viên đang vào lol",
          "Học viên đang choi lol",
          "Học viên đang xem lien minh",
          "Học viên đang pick tướng"
      ],
      "time_allowed": 12,
      "right_choices_count": 1,
      "wrong_choice_values": [0],
      "right_choice_values": [2]
  }
]

# admin
# edit
settings = {
  "reward_frequency": 0.5,
  "initial_quota": 4,
}

# admin
# CRUD
reward_configs = [
  {
    "name": "thẻ cào 20k",
    "quantity": 50,
    "given": 0,
  },
  {
    "name": "áo mindX",
    "quantity": 30,
    "given": 0,
  },
  {
    "name": "Vé xem phim",
    "quantity": 20,
    "given": 0,
  },
]

def generate_quiz(player ,config):
  today_quizzes = [quiz for quiz in player["quizzes"] if quiz["date_sent"] == date.today()]

  today_quota = 0
  if len(today_quizzes) == 0:
    today_quota = 1
  
  quota = today_quota + player["extra_quota"]
  
  if quota <= 0:
    return {"quota": 0, "questions": "Fuck off", "choices": []}
  
  if today_quota == 0:
    player["extra_quota"] -= 1
  
  question = random.choice(config["questions"])
  right_choices_count = config["right_choices_count"]
  wrong_choices = config["wrong_choice_values"] * (9 - right_choices_count)
  right_choices = config["right_choice_values"] * right_choices_count
  choices = wrong_choices + right_choices
  random.shuffle(choices)
  right_choice_indexes = [index for index, choice in enumerate(choices) if choice in right_choices]
  time = config["time_allowed"]
  return {
    "quota": quota - 1,
    "questions": question,
    "choices": choices,
    "time_allowed": time,
    "right_choice_indexes": right_choice_indexes,
    "date_sent": date.today(),
    "time_sent": datetime.now(),
  }

def open_reward(open_times):
  given_reward_list = []
  for _ in range(open_times):
    dice = random.random()
    if dice < settings["reward_frequency"]:
      reward_list = []
      for reward_config in reward_configs:
        if reward_config["quantity"] > reward_config["given"]:
          reward_list += [reward_config] * (reward_config["quantity"] - reward_config["given"])
      reward = random.choice(reward_list)
      reward["given"] += 1
      given_reward_list.append({
        "name": reward["name"]
      })
    else:
      given_reward_list.append({
        "name": "chúc bạn may mắn lần sau"
      })
  return given_reward_list


def check_answer(player, player_choice_indexes):
  today_quizzes = [quiz for quiz in player["quizzes"] if quiz["date_sent"] == date.today()]

  if len(today_quizzes) == 0:
    return "Get /quiz first"
  else:
    today_quiz = today_quizzes[-1]
    player_time_spent = datetime.now() - today_quiz["time_sent"]
    if "player_choice_indexes" in today_quiz:
      return "Already answer"
    elif player_time_spent > timedelta(seconds=today_quiz["time_allowed"]):
      return "too late"
    else:
      today_quiz["player_choice_indexes"] = player_choice_indexes
      if set(player_choice_indexes) == set(today_quiz["right_choice_indexes"]):
        player_seconds_spent = player_time_spent.total_seconds()
        speed = 1 - (player_seconds_spent / today_quiz["time_allowed"])
        if speed > 0.7: # duoi 4stime_sent
          open_times = 3
        elif speed > 0.3: # duoi 9s
          open_times = 2
        else:             # tren 9s
          open_times = 1
        rewards = open_reward(open_times)
        return {
          "correct": True,
          "open_times": open_times,
          "rewards": rewards,
          "right_choice": today_quiz["right_choice_indexes"]
        }
      else:
        return {
          "correct": False,
          "right_choice": today_quiz["right_choice_indexes"]
        }

# def spin_reward():


while True:
  cmd = input("cmd: ").lower().strip()
  if cmd == "login":
    player_name = input("playername").lower()
    found_players = [player for player in players if player["player_name"] == player_name]
    player = None
    if len(found_players) == 0:
      new_player = {"player_name": player_name, "extra_quota": settings["initial_quota"], "quizzes": [], "results": []}
      players.append(new_player)
      player = new_player
      print("Welcome new player")
    else:
      player = found_players[0]
      print("Welcome")
  elif cmd == "quiz":
    quiz_config = random.choice(quiz_configs)
    quiz = generate_quiz(player, quiz_config)
    player["quizzes"].append(quiz)
    player_quiz = quiz.copy()
    print(player_quiz)
  elif cmd == "answer":
    answer = input("Answer? ").strip().split(" ")
    choice_indexes = [int(choice_str) for choice_str in answer if choice_str.isdigit()]
    result = check_answer(player, choice_indexes)
    player["results"].append(result)
    print(result)
  elif cmd == "exit":
    break
