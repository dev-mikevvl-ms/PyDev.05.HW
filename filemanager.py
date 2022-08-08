"""
"Консольный файловый менеджер"

В проекте реализовать следующий функционал:
После запуска программы пользователь видит меню, состоящее из следующих пунктов:
- создать папку;
- удалить (файл/папку);
- копировать (файл/папку);
- просмотр содержимого рабочей директории;
- посмотреть только папки;
- посмотреть только файлы;
- просмотр информации об операционной системе;
- создатель программы;
- играть в викторину;
- мой банковский счет;
- смена рабочей директории (*необязательный пункт);
- выход.
Так же можно добавить любой дополнительный функционал по желанию.
"""
import copy, os, shutil, sys
import itertools as itts
import functools as futs

from mod.MVVlStd import (glSep_s, mInP_FltAVali_fefi, mMenu_c, mSupportsWrite_ca,
    mChe_ExsPath_ff, mCre_AbsPath_ff, mInP_Wai_fp)
import mod.victory, mod.MyBankAcc

# import os
# os.makedirs(name, mode=511, exist_ok=False)
# t_l = os.listdir()
# os.remove(path, *, dir_fd=None)
# os.removedirs(name)
# with os.scandir(path) as it:
#     for entry in it:
#         if not entry.name.startswith('.') and entry.is_file():
#             print(entry.name)
# os.rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None)
# os.link(src, dst, *, src_dir_fd=None, dst_dir_fd=None, follow_symlinks=True)
# os.symlink(src, dst, target_is_directory=False, *, dir_fd=None)
# os.walk(top, topdown=True, onerror=None, followlinks=False)
# os.fwalk(top='.', topdown=True, onerror=None, *, follow_symlinks=False, dir_fd=None)
# os.dup(fd); os.dup2(fd, fd2, inheritable=True)

# mDig_l = ['Создать файл', 'Создать папку', 'Удалить файл', 'Удалить папку',
#  'Копировать файл', 'Копировать папку', 'Про1смотр содержимого рабочей директории',
#  'Посмотреть только папки', 'Посмотреть только файлы']
# mAlpha_l = [ 'Просмотр информации об операционной системе',
#  'Создатель программы', 'Играть в викторину', 'Мой банковский счет',
#  'Смена рабочей директории', 'Выход']
# t_d = dict(**dict((str(_i), [_s, None]) for _i, _s in enumerate(mDig_l, 1)),
#     **dict((_s1, [_s, None]) for _s1, _s in zip('ИЯВБСЫ', mAlpha_l)))
# mMenu_l = list((str(_i), [_s, None]) for _i, _s in enumerate(mDig_l, 1))
# mMainMenu_d = dict(list((str(_i), [_s, None]) for _i, _s in enumerate(mDig_l, 1))
#              + list((_s1, [_s, None]) for _s1, _s in zip('ИЯВБСЫ', mAlpha_l)))
 
mOuPSep_s = '=' *32

# mStt_d = dict(kStkDir_llist[str]=[], kDirEntry_t:tuple[os.DirEntry]=None,
# kTSum_t:tuple(Fi_i, Dir_i, !(Fi|Di)_i, SLnk_i)=None,
# kPreSrtByTyT_t:tuple[tuple[Na_s, Ty_s2:'[DF~][L ]]]=None)
mStt_d = dict(kStkDir_l=[], kDirEntry_t=None, kTSum_t=None, kPreSrtByTyT_t=None)

def mFll_Stt_fe(laNewDir_s=None, laSortKey_cll=lambda _el: _el.name.lower(),
                     laScan_b:bool=True):
  if laNewDir_s is None: laNewDir_s = os.curdir # Init|RScan
  loDir_s = os.path.realpath(laNewDir_s)
  if not os.path.exists(loDir_s):
    raise FileNotFoundError(2, f'Dir:({loDir_s}) not exist.')
    # raise FileNotFoundError(2, f'Dir:({loDir_s}) not exist.', 3)
  if not os.path.isdir(loDir_s):
    raise NotADirectoryError(f'On path:({loDir_s}) exist not directory.')

  if (not bool(mStt_d['kStkDir_l'])) or (mStt_d['kStkDir_l'][-1] != loDir_s):
    mStt_d['kStkDir_l'].append(loDir_s)
    laScan_b = laScan_b or True
  else: pass # SameDir

  if (laScan_b or mStt_d['kDirEntry_t'] is None or mStt_d['kTSum_t'] is None
      or mStt_d['kPreSrtByTyT_t'] is None):
    if callable(laSortKey_cll):
      mStt_d['kDirEntry_t'] = tuple(sorted(os.scandir(loDir_s), key=laSortKey_cll))
    else:
      mStt_d['kDirEntry_t'] = tuple(os.scandir(loDir_s))

    loTIt_t = itts.tee(((_el.name, _el.is_file(), _el.is_dir(), _el.is_symlink())
                        for _el in mStt_d['kDirEntry_t']), 5)
    mStt_d['kTSum_t'] = (sum(_el[1] for _el in loTIt_t[0]), sum(_el[2] for _el in loTIt_t[1]),
        sum((not _el[1] and not _el[2]) for _el in loTIt_t[2]), sum(_el[3] for _el in loTIt_t[3]))
    lo_it = ((_el[0], (('F' if _el[1] else '') or ('D' if _el[2] else '') or "~"), # Srt:DF~, LsPrintableSbl(ASCII):~
                   ('L' if _el[3] else ' ')) for _el in loTIt_t[4])
    mStt_d['kPreSrtByTyT_t'] = tuple((_el[0], (_el[1] + _el[2])) for _el
        in sorted(lo_it, key=lambda _el: _el[1]))

def mOuP_Stt_fmp(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  lo_s = "ТекДиректория:({}), "
  if mStt_d['kDirEntry_t'] is None: lo_s = lo_s.format('')
  else: lo_s = lo_s.format(mStt_d['kStkDir_l'][-1])
  if mStt_d['kDirEntry_t'] is None:
    lo_s += f"All:0"
  elif mStt_d['kTSum_t'] is None:
    lo_s += f"All:{len(mStt_d['kDirEntry_t'])}"
  else:
    lo_s += (f"(All,File,Dir,Oth,+SLink):({len(mStt_d['kDirEntry_t'])}," +
       ','.join(str(_el) for _el in mStt_d['kTSum_t']) + ')')
       
  print(lo_s, file=file)

# InPHstEl:??(fCurDirL_ix, fInP_s, fDesc_s, fRes_a)

def mA_Exit_fm(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  laSf_o.fRunLoop_b = False


# InfoMenuItems
def mA_SysInfo_ffmp(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  loMsg_s = f"{sys.platform=}\n{sys.version=}\n{sys.api_version=}."
  print(mOuPSep_s, loMsg_s, mOuPSep_s, sep='\n', file=file)
  if laSf_o is not None: mInP_Wai_fp(file=file)
  return loMsg_s

def mA_MyInfo_ffmp(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  loMsg_s = "Creator/Author: Mike Vl. Vlasov <dev.mikevvl@outlook.com>."
  print(mOuPSep_s, loMsg_s, mOuPSep_s, sep='\n', file=file)
  if laSf_o is not None: mInP_Wai_fp(file=file)
  return loMsg_s

# OutModItm
def mA_victory_ffmp(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  return mod.victory.main(None)

def mA_MyBankAcc_ffmp(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  return mod.MyBankAcc.main(None, fAFile4Prn_o=file)

# def mA_VieHst_ffmp(laSf_o, file:mSupportsWrite_ca=sys.stdout):
#   print(f"История покупок (всего {len(laSf_o.fOutStt_d['kBuyHstT_l'])} зап.):",
#       *enumerate(laSf_o.fOutStt_d['kBuyHstT_l'], 1), '', sep='\n', file=file)
#   return (laSf_o.fOutStt_d['kAccSum_n'], len(laSf_o.fOutStt_d['kBuyHstT_l']))
#   laSf_o.fInP_s, laSf_o.fInP_k

def mA_Dvl_fm(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  raise OSError('ts')

# print(*(f'{_ix!s:>2}. ({_el[1]}) <{_el[0]}>' for _ix, _el
#      in enumerate(mStt_d['kPreSrtByTyT_t'], 0) if _el[1][0] in 'F~'), '-' *32,
#      *(f'{_ix!s:>2}. {_s}' for _ix, _s in enumerate(f'({_el[1]}) <{_el[0]}>' for _el
#      in mStt_d['kPreSrtByTyT_t'] if _el[1][0] == 'F')), sep='\n')
'''
 2. (F ) <LICENSE>
 3. (F ) <README.md>
 4. (F ) <ts1.py>
 5. (~L) <ts.txt>
--------------------------------
 0. (F ) <LICENSE>
 1. (F ) <README.md>
 2. (F ) <ts1.py>
'''
def mOuP_Vie_fpt(laVie_t, laTDesc1OrMOrNo_t, laHea_s='Fmt:([DF~][L ]) <name>',
    laPau_b=False, file:mSupportsWrite_ca=sys.stdout):
  print(f"In Dir:({mStt_d['kStkDir_l'][-1]}):\n" + mOuPSep_s)
  loCo_i = len(laVie_t)
  if loCo_i == 0:
    print(laTDesc1OrMOrNo_t[-1] + '.\n' + mOuPSep_s, file=file)
  else:
    lo_s = (laTDesc1OrMOrNo_t[0] if loCo_i == 1 else laTDesc1OrMOrNo_t[1])
    if laHea_s is not None: lo_s += f'({laHea_s})'
    print(lo_s + ":", file=file)
    print(*laVie_t, mOuPSep_s, sep='\n', file=file)
  if laPau_b: mInP_Wai_fp(file=file)


def mA_VieAll_fmf(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  lo_t = tuple(f'({_el[1]}) <{_el[0]}>' for _el in mStt_d['kPreSrtByTyT_t'])
  mOuP_Vie_fpt(lo_t, ('One', 'All', 'No files, directories or others'),
      file=file) 
  if laSf_o is not None: mInP_Wai_fp(file=file)
  return lo_t

def mA_VieFi_fmf(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  lo_t = tuple(f'({_el[1]}) <{_el[0]}>' for _el in mStt_d['kPreSrtByTyT_t']
               if _el[1][0] == 'F')
  mOuP_Vie_fpt(lo_t, ('File', 'Files', 'No files'), 
      file=file) 
  if laSf_o is not None: mInP_Wai_fp(file=file)
  return lo_t

def mA_VieDir_fmf(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  lo_t = tuple(f'({_el[1]}) <{_el[0]}>' for _el in mStt_d['kPreSrtByTyT_t']
               if _el[1][0] == 'D')
  mOuP_Vie_fpt(lo_t, ('Directory', 'Directories', 'No directories'),
      file=file) 
  if laSf_o is not None: mInP_Wai_fp(file=file)
  return lo_t

def mA_VieSLnk_fmf(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  lo_t = tuple(f'({_el[1]}) <{_el[0]}>' for _el in mStt_d['kPreSrtByTyT_t']
               if _el[1][-1] == 'L')
  mOuP_Vie_fpt(lo_t, ('Softlink', 'Softlinks', 'No softlinks'),
      file=file) 
      # laPau_b=(laSf_o is not None), file=file) 
  if laSf_o is not None: mInP_Wai_fp(file=file)
  return lo_t

def mA_CreFi_fimpf(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  mA_VieAll_fmf(None, file)
  lo_cll = lambda _s: str(_s) == '' or (str(_s).strip() != ''\
      and not mChe_ExsPath_ff(_s, laCurDir_s=mStt_d['kStkDir_l'][-1]))
  # lo_cll = futs.partial(mChe_ExsPath_ff, laCurDir_s=mStt_d['kDirEntry_t'][-1])
  lo_s = ('файл (каталог или любой\n другой объект файл.системы) '
    + 'с введеным (пустое для возврата в меню)\n именем не должен существовать')
  loRes_s = mInP_FltAVali_fefi(' имя нового файла (абсол. или относит.)\n',
      laInPTypeFlt_cll=None, laValiInPMsg_s=lo_s, laVali_cll=lo_cll,
      laAcceptEmptyInPAsDf_b=True, file=file)[0]
  if loRes_s == '': return None
  loAbsPth_s = mCre_AbsPath_ff(loRes_s, mStt_d['kStkDir_l'][-1])
  # with open(os.path.join(loAbsPth_s), mode='x') as lw_o:
  #   ...
  try:
    loFi_o = open(loAbsPth_s, mode='x')
  except OSError as loExc_o:
    print((f"\tERR: You input:'{loRes_s}' INVALID "
        + f"with exception:({loExc_o}), try again next time."), file=file)
    if laSf_o is not None: mInP_Wai_fp(file=file)
    return str(loExc_o)
  else:
    print(f"\tMSG: You input:'{loRes_s}' and create file:({loAbsPth_s})", file=file)
    if laSf_o is not None: mInP_Wai_fp(file=file)
    mFll_Stt_fe(mStt_d['kStkDir_l'][-1])
    return loAbsPth_s
  # finally:
  #   loFi_o.close()

def mA_CreDir_fimpf(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  mA_VieAll_fmf(None, file)
  lo_cll = lambda _s: str(_s) == '' or (str(_s).strip() != ''\
      and not mChe_ExsPath_ff(_s, laCurDir_s=mStt_d['kStkDir_l'][-1]))
  # lo_cll = futs.partial(mChe_ExsPath_ff, laCurDir_s=mStt_d['kDirEntry_t'][-1])
  lo_s = ('каталог (файл или любой другой\n объект файл.системы) '
    + 'с введеным (пустое для возврата в\n меню) именем не должен существовать')
  loRes_s = mInP_FltAVali_fefi(' имя нового каталога (абсол. или относит.)\n',
      laInPTypeFlt_cll=None, laValiInPMsg_s=lo_s, laVali_cll=lo_cll,
      laAcceptEmptyInPAsDf_b=True, file=file)[0]
  if loRes_s == '': return None
  loAbsPth_s = mCre_AbsPath_ff(loRes_s, mStt_d['kStkDir_l'][-1])
  # with open(os.path.join(loAbsPth_s), mode='x') as lw_o:
  #   ...
  try:
    os.makedirs(loAbsPth_s)
  except OSError as loExc_o:
    print((f"\tERR: You input:'{loRes_s}' INVALID "
        + f"with exception:({loExc_o}), try again next time."), file=file)
    if laSf_o is not None: mInP_Wai_fp(file=file)
    return str(loExc_o)
  else:
    print(f"\tMSG: You input:'{loRes_s}' and create directory:({loAbsPth_s})", file=file)
    if laSf_o is not None: mInP_Wai_fp(file=file)
    mFll_Stt_fe(mStt_d['kStkDir_l'][-1])
    return loAbsPth_s
  # finally:
  #   loFi_o.close()

def mA_ChaCurDi_fimpf(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  mA_VieDir_fmf(None, file)
  lo_cll = lambda _s: str(_s) == '' or (str(_s).strip() != ''\
      and os.path.isdir(mCre_AbsPath_ff(_s, laCurDir_s=mStt_d['kStkDir_l'][-1])))
      # and mChe_ExsPath_ff(_s, laCurDir_s=mStt_d['kStkDir_l'][-1])\
  # lo_cll = futs.partial(mChe_ExsPath_ff, laCurDir_s=mStt_d['kDirEntry_t'][-1])
  lo_s = ('каталог с введеным (пустое для возврата в\n меню) именем должен существовать')
  loRes_s = mInP_FltAVali_fefi(' имя нового каталога (абсол. или относит.)\n',
      laInPTypeFlt_cll=None, laValiInPMsg_s=lo_s, laVali_cll=lo_cll,
      laAcceptEmptyInPAsDf_b=True, file=file)[0]
  if loRes_s == '': return None
  loAbsPth_s = mCre_AbsPath_ff(loRes_s, mStt_d['kStkDir_l'][-1])
  # with open(os.path.join(loAbsPth_s), mode='x') as lw_o:
  #   ...
  try:
    mFll_Stt_fe(loAbsPth_s)
  except OSError as loExc_o:
    print((f"\tERR: You input:'{loRes_s}' INVALID "
        + f"with exception:({loExc_o}), try again next time."), file=file)
    if laSf_o is not None: mInP_Wai_fp(file=file)
    return str(loExc_o)
  else:
    print(f"\tMSG: You input:'{loRes_s}' and change current directory:({loAbsPth_s})", file=file)
    if laSf_o is not None: mInP_Wai_fp(file=file)
    return loAbsPth_s
  # finally:
  #   loFi_o.close()
# mA_ChaCurDi_fimpf(None)
# mOuP_Stt_fmp(None)

# mStt_d = dict(kStkDir_l=[], kDirEntry_t=None, kTSum_t=None)
mMainMenu_d = {
 '0': ('Создать файл', mA_CreFi_fimpf, None), # open(Na, mode='x)
 '1': ('Создать папку', mA_CreDir_fimpf),
 '2': ('Удалить файл', None),
 '3': ('Удалить папку', None),
 '4': ('Копировать файл', None),
 '5': ('Копировать папку', None),
 '6': ('Просмотр содержимого рабочей директории', mA_VieAll_fmf),
 '7': ('Посмотреть только папки', mA_VieDir_fmf),
 '8': ('Посмотреть только файлы', mA_VieFi_fmf),
 '9': ('Посмотреть только ссылки(soft)', mA_VieSLnk_fmf),
 'С': ('Смена рабочей директории', mA_ChaCurDi_fimpf),
 'В': ('Играть в Викторину', mA_victory_ffmp),
 'Б': ('Мой Банковский счет', mA_MyBankAcc_ffmp),
 'И': ('Просмотр Информации об операционной системе', mA_SysInfo_ffmp),
 'Я': ('Я - создатель программы', mA_MyInfo_ffmp, None),
 'Ы': ('ВЫход', mA_Exit_fm),
 'Ф': ('Девел.', mA_Dvl_fm)
 }

def main(laArgV_l: list[str], *laArg_l, **laKwArg_d) -> dict:
  ''' Arg laKMenuCrePP_d=dict(BasePP 4 Cre All Menu In2(Sf))
  '''
  # Ww:laArgV_l(sys.argv[1:])
  # mFll_Stt_fe()
  loRes_o = None
  loCurDir_s = os.path.realpath(os.curdir)
  print('DVL:Beg(CurDir):', os.path.realpath(os.curdir))
  try:
    # mOuP_Stt_fmp(None)
    if len(laArgV_l) == 0: mFll_Stt_fe()
    # elif len(laArgV_l) == 1:  mFll_Stt_fe(laArgV_l[0])
    # else: loRes_b = mFll_Stt_fe(laArgV_l[0])
    else: mFll_Stt_fe(laArgV_l[0])
    # print(1)
    # print(f'DVL:{loRes_b=}')
    # mOuP_Stt_fmp(None)
    if 'laKMenuCrePP_d' in laKwArg_d:
      loKwArg_d = copy.deepcopy(dict(laKwArg_d['laKMenuCrePP_d']))
    else: loKwArg_d = {}
    loAppDesc_s = 'Консольный файловый менеджер'
    loKwArg_d.update(dict(fPrnOutStt_cll=mOuP_Stt_fmp,
        fAppTtl_s=loAppDesc_s))
    loMainMenu_o = mMenu_c(mMainMenu_d, **loKwArg_d)
    # mod.victory.main(None)
    # loRes_o = mod.MyBankAcc.main(None, fAFile4Prn_o=sys.stdout)
    loRes_o = loMainMenu_o()
    print(f'DVL:loRes_o:', *loRes_o, '', sep='\n') #DVL
    # t_l = glStdMsg4InP_l[:]
    # t_l[0] = 'Выберите'
    # print(t_l[0], glStdMsg4InP_l[0])
    # print(mInP_FltAVali_fefi(' пункт меню'))
    return loRes_o
  except Exception as loExc_o:
    print(f'DVL:Exc: {loExc_o}({loExc_o!r})',
        *(f'{_s}:{getattr(loExc_o, _s, None)}' for _s in dir(loExc_o) if not _s.startswith('__')),
        sep='\n')
    raise
  finally:
    # print(f'DVL:loRes_o:', *loRes_o, '', sep='\n') #DVL
    print('DVL:End(CurDir):Bf:', os.path.realpath(os.curdir))
    os.chdir(loCurDir_s)
    print('DVL:End(CurDir):Af:', os.path.realpath(os.curdir))


if __name__ == '__main__':
    # import sys
    main(sys.argv[1:])
    # print(sys.executable, *sys.argv, sep='\n')
    # print('', *sys.orig_argv, sep='\n')
    # main(None)
