import sys
from MVVlStd import glSep_s, inp_FltAVali_fefi
# from mod.MVVlStd import glSep_s, inp_FltAVali_fefi
# from MVVlStd import glSep_s, inp_FltAVali_fefi
# import MVVlStd
# # MVVlStd.inp_FltAVali_fefi('?')
# # inp_FltAVali_fefi('?')

# tTskMsg_s = '''
# Задача 5. МОДУЛЬ 3 файл use_functions.py
# В файле дано описание программы. Предлагается реализовать программу
#  по описанию используя любые средства
# '''
# print(glSep_s, tTskMsg_s, f'{sys.version=}', glSep_s, 'Result:', '',  sep='\n')


class MVVlMenu_c():

      # laIsKeyExit_cll=lambda _sf, _k: int(_k) == max(iter(_sf))
  def __init__(self, laMenuEls_d=None,
      laAccSum_n=0, laHstT_l=None):
    # 2Do: laRet_d{laAccSum_n=0, laHstT_l=None} 4 __call__():return 
    self.MenuEls_d = dict(laMenuEls_d) if laMenuEls_d is not None else {}
    self.AccSum_n = int(laAccSum_n)
    self.HstT_l = laHstT_l if laHstT_l is not None else []
    # self.IsKeyExit_cll = laIsKeyExit_cll
    self.IsRun_b = bool(self.MenuEls_d)

  def __iter__(self): # 2Do: MaB Onl WhiUse(prn_fmp)
    return (_el for _el in sorted(self.MenuEls_d.keys(), key=int))

  # def oup_fmp(self): # 2Do: MaB
  def prn_fmp(self): # 2Do: MaB Onl(9+KeyExit OR Fit2Scr+KeyExit) w/Set(sf.WhiVieElsKey_l)
    if bool(self.MenuEls_d):
      print(glSep_s[:len(glSep_s)//3 *2],
          *(f'{_k}. {_v[0]}' for _k, _v in self.MenuEls_d.items()),
          glSep_s[:len(glSep_s)//3], sep='\n')

  # def oup_Info|Ret_fmp(self):
  # def __str__(self):; __format__; tVieHst_fmp
  def prn_Info_fmp(self):
    print(f'На счету:({self.AccSum_n:.2f}) и в истории покупок {len(self.HstT_l)} зап.',
        glSep_s[:len(glSep_s)//3 *2], sep='\n')

  # def add_Els?_ffm(self):
  # def del_Els?_ffpm(self):
  # def get_Keys?_ffpm(self):

  # def run_ffpm(self):
  def __call__(self):
    while self.IsRun_b:
      self.prn_fmp()
      self.prn_Info_fmp()

      li_s = input('Выберите пункт меню: ')
      if li_s in self.MenuEls_d:
        lo_cll = self.MenuEls_d[li_s][1]
        # if self.IsKeyExit_cll(self, li_s): break
        # if self.IsKeyExit_cll(self, li_s): break
        # if lo_cll is None: break
        if lo_cll is None:
          print(f'DVL: None 4 calling Fu() пункт меню:"{li_s}"')
          continue
        else: loRes_b = lo_cll(self)
      else:
          print(f'Неверный пункт меню:"{li_s}"')
    else:
      # self.prn_Info_fmp()
      print('До свидания!', glSep_s[:len(glSep_s)//3 *2], sep='\n')

    return dict(AccSum_n=self.AccSum_n, HstT_l=self.HstT_l)


def tRefillAcc_fm(self):
  loAdd_n = inp_FltAVali_fefi(f' Ведите сумму на сколько пополнить счет\n',
      laInPTypeFlt_cll=float, laDfV_s='100',
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой\n',
      laVali_cll=lambda _n: 0 <= _n)[0]
  self.AccSum_n += loAdd_n #DVL: input by inp_FltAVali_fefi
  # print(f'DBG: На счету:({self.AccSum_n:.2f}) и в истории покупок {len(self.HstT_l)} зап.')
  return True

def tBuy_fmp(self):
  loCost_n = inp_FltAVali_fefi(f' Введите сумму покупки (на Вашем счету:{self.AccSum_n:.2f})\n',
      laInPTypeFlt_cll=float, laDfV_s=str(min(100, self.AccSum_n)),
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой\n',
      laVali_cll=lambda _n: 0 <= _n)[0]

  if self.AccSum_n < loCost_n: #DVL: input by inp_FltAVali_fefi
    print(f'Денег на Вашем счету:({self.AccSum_n:.2f}) не хватает',
        f' для покупки на сумму:({loCost_n:.2f}).',
        ' Пополните счет, пожалуйста.', sep='\n')
    return False
  
  loDesc_s = inp_FltAVali_fefi(f' Введите название покупки\n', laInPTypeFlt_cll=None,
      laDfV_s="Еда", laAcceptEmptyInPAsDf_b=True)[0]
  
  # print(f'DBG: На счету:({self.AccSum_n}) и в истории покупок {len(self.HstT_l)} зап.')
  self.AccSum_n -= loCost_n
  self.HstT_l.append((loDesc_s, loCost_n)) #DVL: input by inp_FltAVali_fefi
  # print(f'DBG: На счету:({self.AccSum_n}) и в истории покупок {len(self.HstT_l)} зап.')
  return True

def tVieHst_fmp(self):
  print(f'История покупок (всего {len(self.HstT_l)} зап.):',
      *enumerate(self.HstT_l, 1), '', sep='\n')

def tExit_fm(self):
  self.IsRun_b = False
# tMenu_d = {'1':('Пополнение счета', tRefillAcc_fm),
#     '2':('Покупка', tBuy_fm),
#     '3':('История покупок', tVieHst_fm),
#     '4':('Выход', None)}

def main(laArgs: list[str]) -> None:
  tMenu_o = MVVlMenu_c({'1':('Пополнение счета', tRefillAcc_fm),
    '2':('Покупка', tBuy_fmp),
    '3':('История покупок', tVieHst_fmp),
    '4':('Выход', tExit_fm)})
  # tMenu_o = MVVlMenu_c()
  # tMenu_o.add_Els?_ffm(...)
  # tRes_d = tMenu_o.run_ffpm()
  tRes_d = tMenu_o()
  # tRes_d = MVVlMenu_c(...)()
  print(tRes_d)
  


if __name__ == '__main__':
    import sys
    # main(sys.argv[1:])
    main(None)
