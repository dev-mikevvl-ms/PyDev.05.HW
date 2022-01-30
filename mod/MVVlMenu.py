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

# 2Do:
# from dataclasses import dataclass, field
# import copy
# @dataclass
# class D:
#   MenuEls_d: dict = field(default_factory=dict)
#   InnStt_d: dict = field(default_factory=dict)
#   ElsFmt_s: str = '{_k!s:>2}. {_v[0]}'
#   ElFmt_s: str = See(prn_Info_fmp):*(f'{_k}. {self.MenuEls_d[_k][0]}' for _k in self)
#   InnSttFmt_s: str = None # Df |==''> !OuP |> Sf.format(**tInnStt_d)
#   # See(prn_Info_fmp)                                                    '({kAccSum_n:{kWid_i}})'.format(**tInnStt_d)
#   HeaFmt_s: str = None # Df(Rat(glSep_s)) |==''> !OuP |> ??Sf.format(**self.OuPPP_d)
#   FooFmt_s: str = None # Df(Rat(glSep_s)) |==''> !OuP |> ??Sf.format(**self.OuPPP_d)
#   # self.OuPPP_d AllEls_co, VieEls_(co|l), MaxWid_i
#   # x: list = field(default_factory=list)
#   def __post_init__(self):
#     # self.MenuEls_d = copy.deepcopy(dict(self.MenuEls_d))
#     self.MenuEls_d = dict(self.MenuEls_d)
#     self.InnStt_d = copy.deepcopy(dict(self.InnStt_d))
#     self.IsRun_b = bool(self.MenuEls_d)
class MVVlMenu_c():

      # laIsKeyExit_cll=lambda _sf, _k: int(_k) == max(iter(_sf))
  def __init__(self, MenuEls_d=None, InnStt_d=None, PrnInnStt_fmp=None,
      HeaFmt_s=None, FooFmt_s=None, ElsFmt_s='{_k!s:>2}. {_v[0]}'):
    self.MenuEls_d = dict(MenuEls_d) if MenuEls_d is not None else {}
    self.InnStt_d = dict(InnStt_d) if InnStt_d is not None else {}
    self.PrnInnStt_fmp = PrnInnStt_fmp
    self.HeaFmt_s = HeaFmt_s
    self.FooFmt_s = FooFmt_s
    self.ElsFmt_s = ElsFmt_s
    self.IsRun_b = bool(self.MenuEls_d)
    # self.kAccSum_n = int(laAccSum_n)
    # self.kHstT_l = list(laHstT_l) if laHstT_l is not None else []
    # self.IsKeyExit_cll = laIsKeyExit_cll

  def __iter__(self): # 2Do: MaB Onl WhiUse(prn_fmp)
    return (_k for _k in sorted(self.MenuEls_d.keys(), key=int))
  def __getitem__(self, key): # BOf:KISS
      return self.MenuEls_d[key]

  # def oup_fmp(self): # 2Do: MaB
  def prn_fmp(self, file=sys.stdout): # 2Do: MaB Onl(9+KeyExit OR Fit2Scr+KeyExit) w/Set(sf.WhiVieElsKey_l)
    if bool(self.MenuEls_d):
      # print(self.HeaFmt_s, file=file)
      print(glSep_s[:len(glSep_s)//3 *2],
          # *(f'{_k}. {self.MenuEls_d[_k][0]}' for _k in self),
          *(self.ElsFmt_s.format(_k=_k, _v=self[_k]) for _k in self),
          # *(f'{_k}. {_v[0]}' for _k, _v in self.MenuEls_d.items()),
          glSep_s[:len(glSep_s)//3], sep='\n', file=file)
      self.prn_Info_fmp(file=file)
      print(glSep_s[:len(glSep_s)//3 *2], file=file)
      # print(self.FooFmt_s, file=file)

  # def oup_Info|Ret_fmp(self):
  # def __str__(self):; __format__; tVieHst_fmp
  def prn_Info_fmp(self, file=sys.stdout):
    if self.PrnInnStt_fmp and callable(self.PrnInnStt_fmp):
      self.PrnInnStt_fmp(self, laInnStt_d=self.InnStt_d, file=file)
  # def prn_Info_fmp(self, la_d, file=sys.stdout):
  #   print(f"На счету:({la_d['kAccSum_n']:.2f}) и в истории покупок {len(la_d['kHstT_l'])} зап.",
  #       glSep_s[:len(glSep_s)//3 *2], sep='\n', file=file)

  # def add_Els?_ffm(self):
  # def del_Els?_ffpm(self):
  # def get_Keys?_ffpm(self):

  # def run_ffpm(self):
  def __call__(self):
    while self.IsRun_b:
      self.prn_fmp()
      # self.prn_Info_fmp()

      li_s = input(' Выберите пункт меню: ')
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

    return self.InnStt_d

tInnStt_d = dict(kAccSum_n=0, kHstT_l=[])
def tRefillAcc_fm(self, file=sys.stdout):
  # loAdd_n = inp_FltAVali_fefi(f' Введите сумму на сколько пополнить счет\n',
  loAdd_n = inp_FltAVali_fefi(f' сумму на сколько пополнить счет\n',
      laInPTypeFlt_cll=float, laDfV_s='100',
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой\n',
      laVali_cll=lambda _n: 0 <= _n, file=file)[0]
  self.InnStt_d['kAccSum_n'] += loAdd_n #DVL: input by inp_FltAVali_fefi
  # print(f'DBG: На счету:({self.InnStt_d['kAccSum_n']:.2f}) и в истории покупок {len(self.InnStt_d['kHstT_l'])} зап.')
  print(f'Пополнение на:({loAdd_n:.2f}).', file=file)
  return True

def tBuy_fmp(self, file=sys.stdout):
  loCost_n = inp_FltAVali_fefi(f" сумму покупки (на Вашем счету:{self.InnStt_d['kAccSum_n']:.2f})\n",
      laInPTypeFlt_cll=float, laDfV_s=str(min(100, self.InnStt_d['kAccSum_n'])),
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой\n',
      laVali_cll=lambda _n: 0 <= _n, file=file)[0]

  if self.InnStt_d['kAccSum_n'] < loCost_n: #DVL: input by inp_FltAVali_fefi
    print(f"Денег на Вашем счету:({self.InnStt_d['kAccSum_n']:.2f}) не хватает",
        f' для покупки на сумму:({loCost_n:.2f}).',
        ' Пополните счет, пожалуйста.', sep='\n', file=file)
    return False
  
  loDesc_s = inp_FltAVali_fefi(f' название покупки\n', laInPTypeFlt_cll=None,
      laDfV_s="Еда", laAcceptEmptyInPAsDf_b=True, file=file)[0]
  
  # print(f'DBG: На счету:({self.InnStt_d['kAccSum_n']}) и в истории покупок {len(self.InnStt_d['kHstT_l'])} зап.')
  self.InnStt_d['kAccSum_n'] -= loCost_n
  self.InnStt_d['kHstT_l'].append((loDesc_s, loCost_n)) #DVL: input by inp_FltAVali_fefi
  # print(f'DBG: На счету:({self.InnStt_d['kAccSum_n']}) и в истории покупок {len(self.InnStt_d['kHstT_l'])} зап.')
  print(f'Покупка: "{loDesc_s}", на сумму:({loCost_n:.2f}).', file=file)
  return True

def tVieHst_fmp(self, file=sys.stdout):
  print(f"История покупок (всего {len(self.InnStt_d['kHstT_l'])} зап.):",
      *enumerate(self.InnStt_d['kHstT_l'], 1), '', sep='\n', file=file)

def tExit_fm(self):
  self.IsRun_b = False
# tMenu_d = {'1':('Пополнение счета', tRefillAcc_fm, ??Type??(Exit, Back, SbMenu, CtrlVieMenu??)),
#     '2':('Покупка', tBuy_fm),
#     '3':('История покупок', tVieHst_fm),
#     '4':('Выход', None)}

def prn_InnStt_fmp(self, laInnStt_d, file=sys.stdout):
  print(f"На счету:({laInnStt_d['kAccSum_n']:.2f}) и в истории покупок {len(laInnStt_d['kHstT_l'])} зап.",
      # glSep_s[:len(glSep_s)//3 *2], sep='\n',
      file=file)

def main(laArgs: list[str]) -> None:
  tMenu_o = MVVlMenu_c({'1':('Пополнение счета', tRefillAcc_fm),
    '2':('Покупка', tBuy_fmp),
    '3':('История покупок', tVieHst_fmp),
    '4':('Выход', tExit_fm)}, InnStt_d=tInnStt_d, PrnInnStt_fmp=prn_InnStt_fmp)
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
