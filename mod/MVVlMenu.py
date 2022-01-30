import sys
from mod.MVVlStd import glSep_s, inp_FltAVali_fefi
# from MVVlStd import glSep_s, inp_FltAVali_fefi
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
from dataclasses import dataclass, field
from collections.abc import Callable
import copy
@dataclass
class MVVlMenu_c():

  MenuEls_d: dict = field(default_factory=dict)
  InnStt_d: dict = None
  PrnInnStt_fmp: Callable = None # [self, dict, file]; ??Df: IF InnStt_d is !None -> print(InnStt_d)
  HeaFmt_s: str = None
  FooFmt_s: str = None
  ElsFmt_s: str = '{_k!s:>2}. {_v[0]}'
  
  def __post_init__(self):
    # self.MenuEls_d = copy.deepcopy(dict(self.MenuEls_d))
    self.MenuEls_d = dict(self.MenuEls_d)
    if self.InnStt_d is not None:
      self.InnStt_d = copy.deepcopy(dict(self.InnStt_d))
      if self.PrnInnStt_fmp is None:
        self.PrnInnStt_fmp = lambda sf_o, laInnStt_d, file=sys.stdout: print(laInnStt_d, file=file)
    if self.HeaFmt_s is not None: self.HeaFmt_s = str(self.HeaFmt_s)
    else: self.HeaFmt_s = glSep_s[:len(glSep_s)//3 *2]
    if self.FooFmt_s is not None: self.FooFmt_s = str(self.FooFmt_s)
    else: self.FooFmt_s = glSep_s[:len(glSep_s)//3 *2]
    
  #     # laIsKeyExit_cll=lambda _sf, _k: int(_k) == max(iter(_sf))
  # def __init__(self, MenuEls_d=None, InnStt_d=None, PrnInnStt_fmp=None,
  #     HeaFmt_s=None, FooFmt_s=None, ElsFmt_s='{_k!s:>2}. {_v[0]}'):
  #   self.MenuEls_d = dict(MenuEls_d) if MenuEls_d is not None else {}
  #   self.InnStt_d = dict(InnStt_d) if InnStt_d is not None else {}
  #   self.PrnInnStt_fmp = PrnInnStt_fmp
  #   if HeaFmt_s is not None: self.HeaFmt_s = str(HeaFmt_s)
  #   else: self.HeaFmt_s = glSep_s[:len(glSep_s)//3 *2]
  #   if FooFmt_s is not None: self.FooFmt_s = str(FooFmt_s)
  #   else: self.FooFmt_s = glSep_s[:len(glSep_s)//3 *2]
  #   self.ElsFmt_s = ElsFmt_s
    self.IsRun_b = bool(self.MenuEls_d)
    # self.kAccSum_n = int(laAccSum_n)
    # self.kHstT_l = list(laHstT_l) if laHstT_l is not None else []
    # self.IsKeyExit_cll = laIsKeyExit_cll

  def __iter__(self): # 2Do: MaB Onl WhiUse(prn_fmp)
    return (_k for _k in sorted(self.MenuEls_d.keys(), key=int))
  def __getitem__(self, key): # BOf:KISS
      return self.MenuEls_d[key]
  def __len__(self, key): # BOf:KISS
      return len(self.MenuEls_d)

  # def oup_fmp(self): # 2Do: MaB
  def prn_fmp(self, file=sys.stdout): # 2Do: MaB Onl(9+KeyExit OR Fit2Scr+KeyExit) w/Set(sf.WhiVieElsKey_l)
    if bool(self.MenuEls_d):
      if self.HeaFmt_s != '': print(self.HeaFmt_s, file=file)
      print(*(self.ElsFmt_s.format(_k=_k, _v=self[_k]) for _k in self),
          sep='\n', file=file)
      self.prn_Info_fmp(file=file)
      # print(glSep_s[:len(glSep_s)//3 *2], file=file)
      if self.FooFmt_s != '':  print(self.FooFmt_s, file=file)

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

# if __name__ == '__main__':
#     import sys
#     # main(sys.argv[1:])
#     main(None)
