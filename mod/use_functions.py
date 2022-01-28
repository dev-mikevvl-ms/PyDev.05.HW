import sys
from MVVlStd import teSep_s, teInPWTypedWVali_fif

tTskMsg_s = '''
Задача 5. МОДУЛЬ 3 файл use_functions.py
В файле дано описание программы. Предлагается реализовать программу
 по описанию используя любые средства
'''
print(teSep_s, tTskMsg_s, f'{sys.version=}', teSep_s, 'Result:', '',  sep='\n')
"""
МОДУЛЬ 3
Программа "Личный счет"
Описание работы программы:
Пользователь запускает программу у него на счету 0
Программа предлагает следующие варианты действий
1. пополнить счет
2. покупка
3. история покупок
4. выход

1. пополнение счета
при выборе этого пункта пользователю предлагается ввести сумму на сколько пополнить счет
после того как пользователь вводит сумму она добавляется к счету
снова попадаем в основное меню

2. покупка
при выборе этого пункта пользователю предлагается ввести сумму покупки
если она больше количества денег на счете, то сообщаем что денег не хватает и переходим в основное меню
если денег достаточно предлагаем пользователю ввести название покупки, например (еда)
снимаем деньги со счета
сохраняем покупку в историю
выходим в основное меню

3. история покупок
выводим историю покупок пользователя (название и сумму)
возвращаемся в основное меню

4. выход
выход из программы

При выполнении задания можно пользоваться любыми средствами

Для реализации основного меню можно использовать пример ниже или написать свой
"""
glAccSum_n, glHstT_l = 0, []

def tRefillAcc_f():
  global glAccSum_n, glHstT_l
  loAdd_n = teInPWTypedWVali_fif(f' Ведите сумму на сколько пополнить счет',
      laInPTypeFlt_cll=float, laDfV_s='100',
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой',
      laVali_cll=lambda _n: 0 <= _n)[0]
  glAccSum_n += loAdd_n #DVL: input by teInPWTypedWVali_fif
  # print(f'DBG: На счету:({glAccSum_n:.2f}) и в истории покупок {len(glHstT_l)} зап.')
  return True

def tBuy_f():
  global glAccSum_n, glHstT_l
  loCost_n = teInPWTypedWVali_fif(f' Введите сумму покупки (на Вашем счету:{glAccSum_n:.2f})',
      laInPTypeFlt_cll=float, laDfV_s=str(min(100, glAccSum_n)),
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой',
      laVali_cll=lambda _n: 0 <= _n)[0]

  if glAccSum_n < loCost_n: #DVL: input by teInPWTypedWVali_fif
    print(f'Денег на Вашем счету:({glAccSum_n:.2f}) не хватает',
        f'для покупки на сумму:({loCost_n:.2f}).',
        'Пополните счет, пожалуйста.', sep='\n')
    return False
  
  loDesc_s = teInPWTypedWVali_fif(f' Введите название покупки', laInPTypeFlt_cll=None,
      laDfV_s="Еда", laAcceptEmptyInPAsDf_b=True)[0]
  
  # print(f'DBG: На счету:({glAccSum_n}) и в истории покупок {len(glHstT_l)} зап.')
  glAccSum_n -= loCost_n
  glHstT_l.append((loDesc_s, loCost_n)) #DVL: input by teInPWTypedWVali_fif
  # print(f'DBG: На счету:({glAccSum_n}) и в истории покупок {len(glHstT_l)} зап.')
  return True

def tVieHst_f():
  global glAccSum_n, glHstT_l
  print('', f'История покупок (всего {len(glHstT_l)} зап.):',
      *enumerate(glHstT_l, 1), '', sep='\n')

tMenu_d = {'1':('Пополнение счета', tRefillAcc_f),
    '2':('Покупка', tBuy_f),
    '3':('История покупок', tVieHst_f),
    '4':('Выход', None)}

while True:
    print(*(f'{_k}. {_v[0]}' for _k, _v in tMenu_d.items()), sep='\n')
    print(f'На счету:({glAccSum_n:.2f}) и в истории покупок {len(glHstT_l)} зап.')

    li_s = input('Выберите пункт меню: ')
    if li_s in tMenu_d:
      lo_cll = tMenu_d[li_s][1]
      if lo_cll is None: break
      else: loRes_b = lo_cll()
    else:
        print(f'Неверный пункт меню:"{li_s}"')

print(teSep_s)
