import sys
from MVVlStd import glSep_s, inp_FltAVali_feif
# from MVVlStd import glSep_s, inp_FltAVali_feif
# import MVVlStd
# # MVVlStd.inp_FltAVali_feif('?')
# # inp_FltAVali_feif('?')

# tTskMsg_s = '''
# Задача 5. МОДУЛЬ 3 файл use_functions.py
# В файле дано описание программы. Предлагается реализовать программу
#  по описанию используя любые средства
# '''
# print(glSep_s, tTskMsg_s, f'{sys.version=}', glSep_s, 'Result:', '',  sep='\n')

def main(laArgs: list[str]) -> None:
  loAccSum_n, loHstT_l = 0, []

  def tRefillAcc_f():
    global loAccSum_n, loHstT_l
    loAdd_n = inp_FltAVali_feif(f' Ведите сумму на сколько пополнить счет',
        laInPTypeFlt_cll=float, laDfV_s='100',
        laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой',
        laVali_cll=lambda _n: 0 <= _n)[0]
    loAccSum_n += loAdd_n #DVL: input by inp_FltAVali_feif
    # print(f'DBG: На счету:({loAccSum_n:.2f}) и в истории покупок {len(loHstT_l)} зап.')
    return True

  def tBuy_f():
    global loAccSum_n, loHstT_l
    loCost_n = inp_FltAVali_feif(f' Введите сумму покупки (на Вашем счету:{loAccSum_n:.2f})',
        laInPTypeFlt_cll=float, laDfV_s=str(min(100, loAccSum_n)),
        laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой',
        laVali_cll=lambda _n: 0 <= _n)[0]

    if loAccSum_n < loCost_n: #DVL: input by inp_FltAVali_feif
      print(f'Денег на Вашем счету:({loAccSum_n:.2f}) не хватает',
          f'для покупки на сумму:({loCost_n:.2f}).',
          'Пополните счет, пожалуйста.', sep='\n')
      return False
    
    loDesc_s = inp_FltAVali_feif(f' Введите название покупки', laInPTypeFlt_cll=None,
        laDfV_s="Еда", laAcceptEmptyInPAsDf_b=True)[0]
    
    # print(f'DBG: На счету:({loAccSum_n}) и в истории покупок {len(loHstT_l)} зап.')
    loAccSum_n -= loCost_n
    loHstT_l.append((loDesc_s, loCost_n)) #DVL: input by inp_FltAVali_feif
    # print(f'DBG: На счету:({loAccSum_n}) и в истории покупок {len(loHstT_l)} зап.')
    return True

  def tVieHst_f():
    global loAccSum_n, loHstT_l
    print('', f'История покупок (всего {len(loHstT_l)} зап.):',
        *enumerate(loHstT_l, 1), '', sep='\n')

  tMenu_d = {'1':('Пополнение счета', tRefillAcc_f),
      '2':('Покупка', tBuy_f),
      '3':('История покупок', tVieHst_f),
      '4':('Выход', None)}

  while True:
      print(*(f'{_k}. {_v[0]}' for _k, _v in tMenu_d.items()), sep='\n')
      print(f'На счету:({loAccSum_n:.2f}) и в истории покупок {len(loHstT_l)} зап.')

      li_s = input('Выберите пункт меню: ')
      if li_s in tMenu_d:
        lo_cll = tMenu_d[li_s][1]
        if lo_cll is None: break
        else: loRes_b = lo_cll()
      else:
          print(f'Неверный пункт меню:"{li_s}"')



if __name__ == '__main__':
    import sys
    # main(sys.argv[1:])
    main(None)
