"""
Программа викторина будет задавать нам вопросы несколько раз
"""
# 1. Импорт конкретных функций из модуля
# from <название модуля> import нужные функций через ,
# from <название модуля> import нужные функций через ,
import mod.MVVlStd, mod.victory 


def main(laArgs: list[str]) -> None:
  mod.victory.main(None)

if __name__ == '__main__':
    # import sys
    # main(sys.argv[1:])
    main(None)
