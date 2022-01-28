"""
Программа викторина будет задавать нам вопросы несколько раз
"""
# 1. Импорт конкретных функций из модуля
# from <название модуля> import нужные функций через ,
from mod.famous_persons import get_random_person, get_person_and_question


def main(laArgs: list[str]) -> None:

  loTimes_i = int(input('Сколько раз вы хотите играть? '))

  for l_co in range(loTimes_i):
      get_person_and_question()

  print('Пока!')

if __name__ == '__main__':
    # import sys
    # main(sys.argv[1:])
    main(None)
