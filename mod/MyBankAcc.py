import sys
from mod.MVVlStd import glSep_s, inp_FltAVali_fefi, Menu_c
# from mod.MVVlStd import glSep_s, inp_FltAVali_fefi
# from MVVlStd import glSep_s, inp_FltAVali_fefi
# import MVVlStd
# # MVVlStd.inp_FltAVali_fefi('?')
# # inp_FltAVali_fefi('?')
# from mod.MVVlMenu import Menu_c

tInnStt_d = dict(kAccSum_n=0, kHstT_l=[])

def tRefillAcc_fm(self, file=sys.stdout):
  # loAdd_n = inp_FltAVali_fefi(f' Введите сумму на сколько пополнить счет\n',
  loAdd_n = inp_FltAVali_fefi(f' сумму на сколько пополнить счет\n',
      laInPTypeFlt_cll=float, laDfV_s='100.00',
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой\n',
      laVali_cll=lambda _n: 0 <= _n, file=file)[0]
  self.InnStt_d['kAccSum_n'] += loAdd_n #DVL: input by inp_FltAVali_fefi
  # print(f'DBG: На счету:({self.InnStt_d['kAccSum_n']:.2f}) и в истории покупок {len(self.InnStt_d['kHstT_l'])} зап.')
  print(f'Пополнение на:({loAdd_n:.2f}).', file=file)
  return loAdd_n

def tBuy_fmp(self, file=sys.stdout):
  if self.InnStt_d['kAccSum_n'] <= 0:
    print(f"На Вашем счету:({self.InnStt_d['kAccSum_n']:.2f}) <= 0.",
        ' Пополните счет, пожалуйста.', sep='\n', file=file)
    return (None, None)

  loCost_n = inp_FltAVali_fefi(f" сумму покупки (на Вашем счету:{self.InnStt_d['kAccSum_n']:.2f})\n",
      laInPTypeFlt_cll=float, laDfV_s=f"{min(100.00, self.InnStt_d['kAccSum_n']):.2f}",
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой\n',
      laVali_cll=lambda _n: 0 <= _n, file=file)[0]

  if self.InnStt_d['kAccSum_n'] < loCost_n: #DVL: input by inp_FltAVali_fefi
    print(f"Денег на Вашем счету:({self.InnStt_d['kAccSum_n']:.2f}) не хватает",
        f' для покупки на сумму:({loCost_n:.2f}).',
        ' Пополните счет, пожалуйста.', sep='\n', file=file)
    return (None, loCost_n)
  
  loDesc_s = inp_FltAVali_fefi(f' название покупки\n', laInPTypeFlt_cll=None,
      laDfV_s="Еда", laAcceptEmptyInPAsDf_b=True, file=file)[0]
  
  # print(f'DBG: На счету:({self.InnStt_d['kAccSum_n']}) и в истории покупок {len(self.InnStt_d['kHstT_l'])} зап.')
  self.InnStt_d['kAccSum_n'] -= loCost_n
  self.InnStt_d['kHstT_l'].append((loDesc_s, loCost_n)) #DVL: input by inp_FltAVali_fefi
  # print(f'DBG: На счету:({self.InnStt_d['kAccSum_n']}) и в истории покупок {len(self.InnStt_d['kHstT_l'])} зап.')
  print(f'Покупка: "{loDesc_s}", на сумму:({loCost_n:.2f}).', file=file)
  return (loDesc_s, loCost_n)

def tVieHst_fmp(self, file=sys.stdout):
  print(f"История покупок (всего {len(self.InnStt_d['kHstT_l'])} зап.):",
      *enumerate(self.InnStt_d['kHstT_l'], 1), '', sep='\n', file=file)
  return (self.InnStt_d['kAccSum_n'], len(self.InnStt_d['kHstT_l']))

def tExit_fm(self, file=sys.stdout):
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
  # Ww(sys.argv[1:])
  tMenu_o = Menu_c({1:('Пополнение счета', tRefillAcc_fm),
    '2':('Покупка', tBuy_fmp),
    '3':('История покупок', tVieHst_fmp),
    # 'E':('Выход', tExit_fm),
    '4':('Выход', tExit_fm)
    }, InnStt_d=tInnStt_d, PrnInnStt_fmp=prn_InnStt_fmp,
    HeaFmt_s= glSep_s[:len(glSep_s)//3 *2] + '\nМой банковский счет:')
  # tMenu_o = Menu_c()
  # tMenu_o.add_Itm?_ffm(...)
  # tRes_d = tMenu_o.run_ffpm()
  tRes_d = tMenu_o()
  # tRes_d = Menu_c(...)()
  # print(tRes_d)
  return tRes_d
  

if __name__ == '__main__':
    import sys
    # main(sys.argv[1:])
    main(None)
