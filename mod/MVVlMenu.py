# Distributed under the BSD license, version:BSD-3-Clause.
# Copyright © 2022 Mike Vl. Vlasov <dev.mikevvl@outlook.com>.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# See:(https://opensource.org/licenses/BSD-3-Clause).

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
#   MenuItm_d: dict = field(default_factory=dict)
#   InnStt_d: dict = field(default_factory=dict)
#   ItmFmt_s: str = '{_k!s:>2}. {_v[0]}'
#   ElFmt_s: str = See(prn_Info_fmp):*(f'{_k}. {self.MenuItm_d[_k][0]}' for _k in self)
#   InnSttFmt_s: str = None # Df |==''> !OuP |> Sf.format(**tInnStt_d)
#   # See(prn_Info_fmp)                                                    '({kAccSum_n:{kWid_i}})'.format(**tInnStt_d)
#   HeaFmt_s: str = None # Df(Rat(glSep_s)) |==''> !OuP |> ??Sf.format(**self.OuPPP_d)
#   FooFmt_s: str = None # Df(Rat(glSep_s)) |==''> !OuP |> ??Sf.format(**self.OuPPP_d)
#   # self.OuPPP_d AllItm_co, VieItm_(co|l), MaxWid_i
#   # x: list = field(default_factory=list)
#   def __post_init__(self):
#     # self.MenuItm_d = copy.deepcopy(dict(self.MenuItm_d))
#     self.MenuItm_d = dict(self.MenuItm_d)
#     self.InnStt_d = copy.deepcopy(dict(self.InnStt_d))
#     self.IsRun_b = bool(self.MenuItm_d)
from dataclasses import dataclass, field
from collections.abc import Callable
import copy
@dataclass
class Menu_c():

  MenuItm_d: dict = field(default_factory=dict)
  InnStt_d: dict = None
  PrnInnStt_fmp: Callable = None # [self, dict, file]; ??Df: IF InnStt_d is !None -> print(InnStt_d)
  IterSortKey_f: Callable = None # [key] ??(Prop4Set): AsIn2MenuItm_d OR (lambda _el: str(_el))|int
  HeaFmt_s: str = None
  FooFmt_s: str = None
  ItmFmt_s: str = '{_k!s:>2}. {_v[0]}'
  
  def __post_init__(self):
    # self.MenuItm_d = copy.deepcopy(dict(self.MenuItm_d))
    self.MenuItm_d = dict(self.MenuItm_d)
    if self.InnStt_d is not None:
      self.InnStt_d = copy.deepcopy(dict(self.InnStt_d))
      if self.PrnInnStt_fmp is None:
        self.PrnInnStt_fmp = lambda sf_o, laInnStt_d, file=sys.stdout: print(laInnStt_d, file=file)
    if self.HeaFmt_s is not None: self.HeaFmt_s = str(self.HeaFmt_s)
    else: self.HeaFmt_s = glSep_s[:len(glSep_s)//3 *2]
    if self.FooFmt_s is not None: self.FooFmt_s = str(self.FooFmt_s)
    else: self.FooFmt_s = glSep_s[:len(glSep_s)//3 *2]
    
  #     # laIsKeyExit_cll=lambda _sf, _k: int(_k) == max(iter(_sf))
  # def __init__(self, MenuItm_d=None, InnStt_d=None, PrnInnStt_fmp=None,
  #     HeaFmt_s=None, FooFmt_s=None, ItmFmt_s='{_k!s:>2}. {_v[0]}'):
  #   self.MenuItm_d = dict(MenuItm_d) if MenuItm_d is not None else {}
  #   self.InnStt_d = dict(InnStt_d) if InnStt_d is not None else {}
  #   self.PrnInnStt_fmp = PrnInnStt_fmp
  #   if HeaFmt_s is not None: self.HeaFmt_s = str(HeaFmt_s)
  #   else: self.HeaFmt_s = glSep_s[:len(glSep_s)//3 *2]
  #   if FooFmt_s is not None: self.FooFmt_s = str(FooFmt_s)
  #   else: self.FooFmt_s = glSep_s[:len(glSep_s)//3 *2]
  #   self.ItmFmt_s = ItmFmt_s
    self.IsRun_b = bool(self.MenuItm_d)
    # self.kAccSum_n = int(laAccSum_n)
    # self.kHstT_l = list(laHstT_l) if laHstT_l is not None else []
    # self.IsKeyExit_cll = laIsKeyExit_cll

  def __iter__(self): # 2Do: MaB Onl WhiUse(prn_fmp)
    if self.IterSortKey_f is None:
      return (_k for _k in self.MenuItm_d.keys())
    return (_k for _k in sorted(self.MenuItm_d.keys(), key=self.IterSortKey_f))
  def __getitem__(self, key): # BOf:KISS
    return self.MenuItm_d[key]
  def __len__(self): # BOf:KISS
    return len(self.MenuItm_d)
  def __contains__(self, key): # BOf:KISS
    return key in self.MenuItm_d

  # def oup_fmp(self): # 2Do: MaB
  def prn_fmp(self, file=sys.stdout): # 2Do: MaB Onl(9+KeyExit OR Fit2Scr+KeyExit) w/Set(sf.WhiVieItmKey_l)
    if bool(self.MenuItm_d):
      if self.HeaFmt_s != '': print(self.HeaFmt_s, file=file)
      print(*(self.ItmFmt_s.format(_k=_k, _v=self[_k]) for _k in self),
          sep='\n', file=file)
      self.prn_Info_fmp(file=file)
      # print(glSep_s[:len(glSep_s)//3 *2], file=file)
      if self.FooFmt_s != '': print(self.FooFmt_s, file=file)

  # def oup_Info|Ret_fmp(self):
  # def __str__(self):; __format__; tVieHst_fmp
  def prn_Info_fmp(self, file=sys.stdout):
    if self.PrnInnStt_fmp and callable(self.PrnInnStt_fmp):
      self.PrnInnStt_fmp(self, laInnStt_d=self.InnStt_d, file=file)
  # def prn_Info_fmp(self, la_d, file=sys.stdout):
  #   print(f"На счету:({la_d['kAccSum_n']:.2f}) и в истории покупок {len(la_d['kHstT_l'])} зап.",
  #       glSep_s[:len(glSep_s)//3 *2], sep='\n', file=file)

  # def add_Itm?_ffm(self):
  # def del_Itm?_ffpm(self):
  # def get_Keys?_ffpm(self):

  # def run_ffpm(self):
  def __call__(self, file=sys.stdout):
    while self.IsRun_b:
      self.prn_fmp(file=file)
      # self.prn_Info_fmp()
      # loMax
      # li_s = input(' Выберите пункт меню: ')
      li_s = inp_FltAVali_fefi(f' пункт меню', laInPTypeFlt_cll=None,
          file=file)[0].strip()
      # if li_s in self.MenuItm_d:
      if li_s in self:
        li_k = li_s
      else:
        try: 
          li_k = int(li_s)
        except ValueError as le_o:
          li_k = None
        else:
          if li_k not in self: li_k = None
      if li_k is not None:
        # lo_cll = self.MenuItm_d[li_s][1]
        lo_cll = self[li_k][1]
        # if self.IsKeyExit_cll(self, li_s): break
        # if lo_cll is None: break
        if lo_cll is None: # 2Do:AddHst
          print(f'DVL: None 4 calling Fu() пункт меню:"{li_k}"')
          continue
        else: loRes_a = lo_cll(self, file=file) # 2Do:AddHst
      else:
          print(f'Неверный пункт меню:"{li_s}"') # 2Do:AddHst
    else: # 2Do:AddHst
      # self.prn_Info_fmp()
      if self.HeaFmt_s != '': print(self.HeaFmt_s, file=file)
      print('До свидания!')
      if self.FooFmt_s != '': print(self.FooFmt_s, file=file)
    return self.InnStt_d # 2Do:RetHst

# if __name__ == '__main__':
#     import sys
#     # main(sys.argv[1:])
#     main(None)
