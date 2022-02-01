import copy, sys
# from mod.MVVlStd import glSep_s, inp_FltAVali_fefi, Menu_c
from mod.MVVlStd import glSep_s, inp_FltAVali_fefi
# import mod.MVVlStd
# from mod.MVVlStd import glSep_s, inp_FltAVali_fefi
# from MVVlStd import glSep_s, inp_FltAVali_fefi
# import MVVlStd
# # MVVlStd.inp_FltAVali_fefi('?')
# # inp_FltAVali_fefi('?')
# from mod.MVVlMenu import Menu_c
import copy, sys, time
from dataclasses import dataclass, field
from collections.abc import Callable

# Frz: Menu_c Bf:Cha(mod.MVVlStd)
@dataclass
class Menu_c():

  fMenuItm_d: dict = field(default_factory=dict)
  fOutStt_d: dict = None
  fPrnOutStt_cll: Callable = None # [self, dict, file]; ??Df: IF fOutStt_d is !None -> print(fOutStt_d)
  fIterSortKey_cll: Callable = None # [key] ??(Prop4Set): AsIn2fMenuItm_d OR (lambda _el: str(_el))|int
  fHeaFmt_s: str = None
  fFooFmt_s: str = None
  fItmFmt_s: str = '{_k!s:>2}. {_v[0]}'
  fAddHst_b: bool = True
  fFile_o: object = sys.stdout

  def __post_init__(self):
    self.fMenuItm_d = dict(self.fMenuItm_d)
    if self.fOutStt_d is not None:
      self.fOutStt_d = copy.deepcopy(dict(self.fOutStt_d))
      if self.fPrnOutStt_cll is None:
        self.fPrnOutStt_cll = lambda sf_o, lafOutStt_d, file=self.fFile_o: print(lafOutStt_d, file=file)
    if self.fHeaFmt_s is not None: self.fHeaFmt_s = str(self.fHeaFmt_s)
    else: self.fHeaFmt_s = glSep_s
    if self.fFooFmt_s is not None: self.fFooFmt_s = str(self.fFooFmt_s)
    else: self.fFooFmt_s = glSep_s[:len(glSep_s)//3 *2]
    
    self.fRunLoop_b = bool(self.fMenuItm_d)
    if self.fAddHst_b:
      if self.fOutStt_d is None:
        self.fOutStt_d = {'kActHst_l':[]}
      if 'kActHst_l' not in self.fOutStt_d:
        self.fOutStt_d['kActHst_l'] = []
      self.fActHst_l = self.fOutStt_d['kActHst_l']
      self.fActHst_l.append((time.time_ns(), 'Inn', '__post_init__', True))
    else:
      self.fActHst_l = None

  def __iter__(self): # 2Do: MaB Onl WhiUse(prn_fmp)
    if self.fIterSortKey_cll is None:
      return (_k for _k in self.fMenuItm_d.keys())
    return (_k for _k in sorted(self.fMenuItm_d.keys(), key=self.fIterSortKey_cll))

  def __getitem__(self, key): # BOf:KISS
    return self.fMenuItm_d[key]

  def __len__(self): # BOf:KISS
    return len(self.fMenuItm_d)

  def __contains__(self, key): # BOf:KISS
    return key in self.fMenuItm_d

  # 2Do: MaB: oup_fmp(self, file=fFile_o)
  # 2Do: MaB Onl(9+KeyExit OR Fit2Scr+KeyExit) w/Set(sf.WhiVieItmKey_l)
  def prn_fmp(self, file=fFile_o):
    if bool(self.fMenuItm_d):
      if self.fHeaFmt_s != '': print(self.fHeaFmt_s, file=file)
      print(*(self.fItmFmt_s.format(_k=_k, _v=self[_k]) for _k in self),
          sep='\n', file=file)
      self.prn_Info_fmp(file=file)
      if self.fFooFmt_s != '': print(self.fFooFmt_s, file=file)

  # def __str__(self):; __format__; tVieHst_fmp
  def prn_Info_fmp(self, file=fFile_o):
    if self.fPrnOutStt_cll and callable(self.fPrnOutStt_cll):
      self.fPrnOutStt_cll(self, laOutStt_d=self.fOutStt_d, file=file)

  # def add_Itms?_ffm(self):
  # def del_Itms?_ffpm(self):
  # def get_Keys?_ffpm(self):

  # def run_ffpm(self):
  def __call__(self, file=fFile_o): # MainLoop
    if self.fActHst_l is not None:
      self.fActHst_l.append((time.time_ns(), 'Inn', 'Beg:MainLoop', True))
    while self.fRunLoop_b:
      self.prn_fmp(file=file)
      li_s = inp_FltAVali_fefi(f' пункт меню', laInPTypeFlt_cll=None,
          file=file)[0].strip()
      if li_s in self:
        li_k = li_s
      else:
        try: li_k = int(li_s)
        except ValueError as le_o: li_k = None
        else:
          if li_k not in self: li_k = None
      if li_k is not None:
        lo_cll = self[li_k][1]
        if lo_cll is None: # 2Do:AddHst
          print(f'DVL: None 4 calling Fu() пункт меню({li_k})', file=file)
          continue
        else:
          loRes_a = lo_cll(self, file=file) # 2Do:AddHst
          if self.fActHst_l is not None:
            self.fActHst_l.append((time.time_ns(), 'InP',
                f'({li_s})' + self[li_k][0], loRes_a))
      else:
          print(f'Неверный пункт меню({li_s})', file=file) # 2Do:AddHst
    else: # 2Do:AddHst
      if self.fHeaFmt_s != '': print(self.fHeaFmt_s, file=file)
      print('До свидания!', file=file)
      if self.fActHst_l is not None:
        self.fActHst_l.append((time.time_ns(), 'Inn', 'End:MainLoop', True))
      if self.fFooFmt_s != '': print(self.fFooFmt_s, file=file)

    return self.fOutStt_d # 2Do:RetHst

tOutStt_d = dict(kAccSum_n=0, kBuyHstT_l=[])

def tRefillAcc_ffp(laSf_o, file=sys.stdout):
  # loAdd_n = inp_FltAVali_fefi(f' Введите сумму на сколько пополнить счет\n',
  loAdd_n = inp_FltAVali_fefi(f' сумму на сколько пополнить счет\n',
      laInPTypeFlt_cll=float, laDfV_s='100.00',
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой\n',
      laVali_cll=lambda _n: 0 <= _n, file=file)[0]
  laSf_o.fOutStt_d['kAccSum_n'] += loAdd_n #DVL: input by inp_FltAVali_fefi
  # print(f'DBG: На счету:({laSf_o.fOutStt_d['kAccSum_n']:.2f}) и в истории покупок {len(laSf_o.fOutStt_d['kBuyHstT_l'])} зап.')
  print(f'Пополнение на:({loAdd_n:.2f}).', file=file)
  return loAdd_n

def tBuy_ffp(laSf_o, file=sys.stdout):
  if laSf_o.fOutStt_d['kAccSum_n'] <= 0:
    print(f"На Вашем счету:({laSf_o.fOutStt_d['kAccSum_n']:.2f}) <= 0.",
        ' Пополните счет, пожалуйста.', sep='\n', file=file)
    return (None, None)

  loCost_n = inp_FltAVali_fefi(f" сумму покупки (на Вашем счету:{laSf_o.fOutStt_d['kAccSum_n']:.2f})\n",
      laInPTypeFlt_cll=float, laDfV_s=f"{min(100.00, laSf_o.fOutStt_d['kAccSum_n']):.2f}",
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой\n',
      laVali_cll=lambda _n: 0 <= _n, file=file)[0]

  if laSf_o.fOutStt_d['kAccSum_n'] < loCost_n: #DVL: input by inp_FltAVali_fefi
    print(f"Денег на Вашем счету:({laSf_o.fOutStt_d['kAccSum_n']:.2f}) не хватает",
        f' для покупки на сумму:({loCost_n:.2f}).',
        ' Пополните счет, пожалуйста.', sep='\n', file=file)
    return (None, loCost_n)
  
  loDesc_s = inp_FltAVali_fefi(f' название покупки\n', laInPTypeFlt_cll=None,
      laDfV_s="Еда", laAcceptEmptyInPAsDf_b=True, file=file)[0]
  
  # print(f'DBG: На счету:({laSf_o.fOutStt_d['kAccSum_n']}) и в истории покупок {len(laSf_o.fOutStt_d['kBuyHstT_l'])} зап.')
  laSf_o.fOutStt_d['kAccSum_n'] -= loCost_n
  laSf_o.fOutStt_d['kBuyHstT_l'].append((loDesc_s, loCost_n)) #DVL: input by inp_FltAVali_fefi
  # print(f'DBG: На счету:({laSf_o.fOutStt_d['kAccSum_n']}) и в истории покупок {len(laSf_o.fOutStt_d['kBuyHstT_l'])} зап.')
  print(f'Покупка: "{loDesc_s}", на сумму:({loCost_n:.2f}).', file=file)
  return (loDesc_s, loCost_n)

def tVieHst_ffp(laSf_o, file=sys.stdout):
  print(f"История покупок (всего {len(laSf_o.fOutStt_d['kBuyHstT_l'])} зап.):",
      *enumerate(laSf_o.fOutStt_d['kBuyHstT_l'], 1), '', sep='\n', file=file)
  return (laSf_o.fOutStt_d['kAccSum_n'], len(laSf_o.fOutStt_d['kBuyHstT_l']))

def tExit_f(laSf_o, file=sys.stdout):
  laSf_o.fRunLoop_b = False

# tMenu_d = {'1':('Пополнение счета', tRefillAcc_ffp, ??Type??(Exit, Back, SbMenu, CtrlVieMenu??)),
#     '2':('Покупка', tBuy_fm),
#     '3':('История покупок', tVieHst_fm),
#     '4':('Выход', None)}

def prn_OutStt_fp(laSf_o, laOutStt_d, file=sys.stdout):
  # 2Do: CheExs(kAccSum_n, kBuyHstT_l)
  if 'kAccSum_n' in laOutStt_d and 'kBuyHstT_l' in laOutStt_d:
    print(f"На счету:({laOutStt_d['kAccSum_n']:.2f})",
        f"и в истории покупок {len(laOutStt_d['kBuyHstT_l'])} зап.",
        # glSep_s[:len(glSep_s)//3 *2], sep='\n',
        file=file)

def main(laArgs: list[str], *laArg_l, **laKwArg_d) -> dict:
  ''' Arg laKMenuCrePP_d=dict(BasePP 4 Cre All Menu In2(Sf))
      Will UseW(.deepcopy)
  '''
  # Ww:laArgs(sys.argv[1:])
  if 'laKMenuCrePP_d' in laKwArg_d:
    loKwArg_d = copy.deepcopy(dict(laKwArg_d['laKMenuCrePP_d']))
  else: loKwArg_d = {}
  loAppDesc_s = 'Мой банковский счет'
  loKwArg_d.update(dict(fOutStt_d=tOutStt_d, fPrnOutStt_cll=prn_OutStt_fp,
      fHeaFmt_s= glSep_s + f'\n{loAppDesc_s}:'))
  ''' Arg laKMenuCrePP_d=dict(PP 4 Upd:PP(Cre All Menu In2(Sf)))
  '''
  # # Ww:laArgs(sys.argv[1:])
  # loKwArg_d = dict(fOutStt_d=tOutStt_d, fPrnOutStt_cll=prn_OutStt_fp,
  #     fHeaFmt_s= glSep_s + '\nМой банковский счет:')
  # if 'laKMenuCrePP_d' in laKwArg_d:
  #   loKwArg_d.update(laKwArg_d['laKMenuCrePP_d'])
  tMenu_o = Menu_c({1:('Пополнение счета', tRefillAcc_ffp),
    '2':('Покупка', tBuy_ffp),
    '3':('История покупок', tVieHst_ffp),
    # 'E':('Выход', tExit_f),
    '4':('Выход', tExit_f)
    }, **loKwArg_d)
    # HeaFmt_s= glSep_s[:len(glSep_s)//3 *2] + '\nМой банковский счет:')
  # tMenu_o = Menu_c()
  # tMenu_o.add_Itm?_ffm(...)
  # tRes_d = tMenu_o.run_ffpm()
  tRes_d = tMenu_o()
  # tRes_d = Menu_c(...)()
  print(tRes_d)
  return tRes_d
  

if __name__ == '__main__':
    import sys
    # main(sys.argv[1:])
    main(None)
