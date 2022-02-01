import copy, sys
from mod.MVVlStd import glSep_s, inp_FltAVali_fefi, Menu_c
import mod.MVVlStd
# from mod.MVVlStd import glSep_s, inp_FltAVali_fefi
# from MVVlStd import glSep_s, inp_FltAVali_fefi
# import MVVlStd
# # MVVlStd.inp_FltAVali_fefi('?')
# # inp_FltAVali_fefi('?')
# from mod.MVVlMenu import Menu_c

tInnStt_d = dict(kAccSum_n=0, kBuyHstT_l=[])

def tRefillAcc_ffp(laSf_o, file=sys.stdout):
  # loAdd_n = inp_FltAVali_fefi(f' Введите сумму на сколько пополнить счет\n',
  loAdd_n = inp_FltAVali_fefi(f' сумму на сколько пополнить счет\n',
      laInPTypeFlt_cll=float, laDfV_s='100.00',
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой\n',
      laVali_cll=lambda _n: 0 <= _n, file=file)[0]
  laSf_o.fInnStt_d['kAccSum_n'] += loAdd_n #DVL: input by inp_FltAVali_fefi
  # print(f'DBG: На счету:({laSf_o.fInnStt_d['kAccSum_n']:.2f}) и в истории покупок {len(laSf_o.fInnStt_d['kBuyHstT_l'])} зап.')
  print(f'Пополнение на:({loAdd_n:.2f}).', file=file)
  return loAdd_n

def tBuy_ffp(laSf_o, file=sys.stdout):
  if laSf_o.fInnStt_d['kAccSum_n'] <= 0:
    print(f"На Вашем счету:({laSf_o.fInnStt_d['kAccSum_n']:.2f}) <= 0.",
        ' Пополните счет, пожалуйста.', sep='\n', file=file)
    return (None, None)

  loCost_n = inp_FltAVali_fefi(f" сумму покупки (на Вашем счету:{laSf_o.fInnStt_d['kAccSum_n']:.2f})\n",
      laInPTypeFlt_cll=float, laDfV_s=f"{min(100.00, laSf_o.fInnStt_d['kAccSum_n']):.2f}",
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой\n',
      laVali_cll=lambda _n: 0 <= _n, file=file)[0]

  if laSf_o.fInnStt_d['kAccSum_n'] < loCost_n: #DVL: input by inp_FltAVali_fefi
    print(f"Денег на Вашем счету:({laSf_o.fInnStt_d['kAccSum_n']:.2f}) не хватает",
        f' для покупки на сумму:({loCost_n:.2f}).',
        ' Пополните счет, пожалуйста.', sep='\n', file=file)
    return (None, loCost_n)
  
  loDesc_s = inp_FltAVali_fefi(f' название покупки\n', laInPTypeFlt_cll=None,
      laDfV_s="Еда", laAcceptEmptyInPAsDf_b=True, file=file)[0]
  
  # print(f'DBG: На счету:({laSf_o.fInnStt_d['kAccSum_n']}) и в истории покупок {len(laSf_o.fInnStt_d['kBuyHstT_l'])} зап.')
  laSf_o.fInnStt_d['kAccSum_n'] -= loCost_n
  laSf_o.fInnStt_d['kBuyHstT_l'].append((loDesc_s, loCost_n)) #DVL: input by inp_FltAVali_fefi
  # print(f'DBG: На счету:({laSf_o.fInnStt_d['kAccSum_n']}) и в истории покупок {len(laSf_o.fInnStt_d['kBuyHstT_l'])} зап.')
  print(f'Покупка: "{loDesc_s}", на сумму:({loCost_n:.2f}).', file=file)
  return (loDesc_s, loCost_n)

def tVieHst_ffp(laSf_o, file=sys.stdout):
  print(f"История покупок (всего {len(laSf_o.fInnStt_d['kBuyHstT_l'])} зап.):",
      *enumerate(laSf_o.fInnStt_d['kBuyHstT_l'], 1), '', sep='\n', file=file)
  return (laSf_o.fInnStt_d['kAccSum_n'], len(laSf_o.fInnStt_d['kBuyHstT_l']))

def tExit_f(laSf_o, file=sys.stdout):
  laSf_o.fRunLoop_b = False

# tMenu_d = {'1':('Пополнение счета', tRefillAcc_ffp, ??Type??(Exit, Back, SbMenu, CtrlVieMenu??)),
#     '2':('Покупка', tBuy_fm),
#     '3':('История покупок', tVieHst_fm),
#     '4':('Выход', None)}

def prn_InnStt_fp(laSf_o, laInnStt_d, file=sys.stdout):
  # 2Do: CheExs(kAccSum_n, kBuyHstT_l)
  if 'kAccSum_n' in laInnStt_d and 'kBuyHstT_l' in laInnStt_d:
    print(f"На счету:({laInnStt_d['kAccSum_n']:.2f})",
        f"и в истории покупок {len(laInnStt_d['kBuyHstT_l'])} зап.",
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
  loKwArg_d.update(dict(fInnStt_d=tInnStt_d, fPrnInnStt_cll=prn_InnStt_fp,
      fHeaFmt_s= mod.MVVlStd.glSep_s + f'\n{loAppDesc_s}:'))
  ''' Arg laKMenuCrePP_d=dict(PP 4 Upd:PP(Cre All Menu In2(Sf)))
  '''
  # # Ww:laArgs(sys.argv[1:])
  # loKwArg_d = dict(fInnStt_d=tInnStt_d, fPrnInnStt_cll=prn_InnStt_fp,
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
