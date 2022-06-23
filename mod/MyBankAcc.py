import copy, sys
from mod.MVVlStd import glSep_s, inp_FltAVali_fefi, Menu_c

mOutStt_d = dict(kAccSum_n=0, kBuyHstT_l=[])

def mA_RefillAcc_ffmp(laSf_o, file=sys.stdout):
  # loAdd_n = inp_FltAVali_fefi(f' Введите сумму на сколько пополнить счет\n',
  loAdd_n = inp_FltAVali_fefi(f' сумму на сколько пополнить счет\n',
      laInPTypeFlt_cll=float, laDfV_s='100.00',
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой\n',
      laVali_cll=lambda _n: 0 <= _n, file=file)[0]
  mOutStt_d['kAccSum_n'] += loAdd_n #DVL: input by inp_FltAVali_fefi
  # print(f'DBG: На счету:({mOutStt_d['kAccSum_n']:.2f}) и в истории покупок {len(mOutStt_d['kBuyHstT_l'])} зап.')
  print(f'Пополнение на:({loAdd_n:.2f}).', file=file)
  return loAdd_n

def mA_Buy_ffmp(laSf_o, file=sys.stdout):
  if mOutStt_d['kAccSum_n'] <= 0:
    print(f"На Вашем счету:({mOutStt_d['kAccSum_n']:.2f}) <= 0.",
        ' Пополните счет, пожалуйста.', sep='\n', file=file)
    return (None, None)

  loCost_n = inp_FltAVali_fefi(f" сумму покупки (на Вашем счету:{mOutStt_d['kAccSum_n']:.2f})\n",
      laInPTypeFlt_cll=float, laDfV_s=f"{min(100.00, mOutStt_d['kAccSum_n']):.2f}",
      laAcceptEmptyInPAsDf_b=True, laValiInPMsg_s=f'положительное число с возм.десят.точкой\n',
      laVali_cll=lambda _n: 0 <= _n, file=file)[0]

  if mOutStt_d['kAccSum_n'] < loCost_n: #DVL: input by inp_FltAVali_fefi
    print(f"Денег на Вашем счету:({mOutStt_d['kAccSum_n']:.2f}) не хватает",
        f' для покупки на сумму:({loCost_n:.2f}).',
        ' Пополните счет, пожалуйста.', sep='\n', file=file)
    return (None, loCost_n)
  
  loDesc_s = inp_FltAVali_fefi(f' название покупки\n', laInPTypeFlt_cll=None,
      laDfV_s="Еда", laAcceptEmptyInPAsDf_b=True, file=file)[0]
  
  # print(f'DBG: На счету:({mOutStt_d['kAccSum_n']}) и в истории покупок {len(mOutStt_d['kBuyHstT_l'])} зап.')
  mOutStt_d['kAccSum_n'] -= loCost_n
  mOutStt_d['kBuyHstT_l'].append((loDesc_s, loCost_n)) #DVL: input by inp_FltAVali_fefi
  # print(f'DBG: На счету:({mOutStt_d['kAccSum_n']}) и в истории покупок {len(mOutStt_d['kBuyHstT_l'])} зап.')
  print(f'Покупка: "{loDesc_s}", на сумму:({loCost_n:.2f}).', file=file)
  return (loDesc_s, loCost_n)

def mA_VieHst_ffmp(laSf_o, file=sys.stdout):
  print(f"История покупок (всего {len(mOutStt_d['kBuyHstT_l'])} зап.):",
      *enumerate(mOutStt_d['kBuyHstT_l'], 1), '', sep='\n', file=file)
  return (mOutStt_d['kAccSum_n'], len(mOutStt_d['kBuyHstT_l']))

def mA_Exit_fm(laSf_o, file=sys.stdout):
  laSf_o.fRunLoop_b = False

# tMenu_d = {'1':('Пополнение счета', mA_RefillAcc_ffmp, ??Type??(Exit, Back, SbMenu, CtrlVieMenu??)),
#     '2':('Покупка', tBuy_fm),
#     '3':('История покупок', tVieHst_fm),
#     '4':('Выход', None)}

def mOuP_Stt_fmp(laSf_o, file=sys.stdout):
  # 2Do: CheExs(kAccSum_n, kBuyHstT_l)
  if 'kAccSum_n' in mOutStt_d and 'kBuyHstT_l' in mOutStt_d:
    print(f"На счету:({mOutStt_d['kAccSum_n']:.2f})",
        f"и в истории покупок {len(mOutStt_d['kBuyHstT_l'])} зап.",
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
  # loKwArg_d.update(dict(fOutStt_d=mOutStt_d, fPrnOutStt_cll=mOuP_Stt_fmp,
  #     fHeaFmt_s= glSep_s + f'\n{loAppDesc_s}:'))
  loKwArg_d.update(dict(fPrnOutStt_cll=mOuP_Stt_fmp,
      fHeaFmt_s= glSep_s + f'\n{loAppDesc_s}:'))
  ''' Arg laKMenuCrePP_d=dict(PP 4 Upd:PP(Cre All Menu In2(Sf)))
  '''
  # # Ww:laArgs(sys.argv[1:])
  # loKwArg_d = dict(fOutStt_d=mOutStt_d, fPrnOutStt_cll=mOuP_Stt_fmp,
  #     fHeaFmt_s= glSep_s + '\nМой банковский счет:')
  # if 'laKMenuCrePP_d' in laKwArg_d:
  #   loKwArg_d.update(laKwArg_d['laKMenuCrePP_d'])
  loMenu_o = Menu_c({1:('Пополнение счета', mA_RefillAcc_ffmp),
    '2':('Покупка', mA_Buy_ffmp),
    '3':('История покупок', mA_VieHst_ffmp),
    # 'E':('Выход', mA_Exit_fm),
    '4':('Выход', mA_Exit_fm)
    }, **loKwArg_d)
    # HeaFmt_s= glSep_s[:len(glSep_s)//3 *2] + '\nМой банковский счет:')
  # loMenu_o = Menu_c()
  # loMenu_o.add_Itm?_ffm(...)
  # loRes_o = loMenu_o.run_ffpm()
  loRes_o = loMenu_o()
  # loRes_o = Menu_c(...)()
  print(loRes_o) #DVL
  return loRes_o
  

if __name__ == '__main__':
    import sys
    # main(sys.argv[1:])
    main(None)
