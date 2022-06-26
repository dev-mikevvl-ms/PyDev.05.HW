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

from mod.MVVlStd import glSep_s, mInP_FltAVali_fefi, mMenu_c, mSupportsWrite_ca
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
 
# mStt_d = dict(kRtDir_s=None, kCurRelDir_s=None, kDirEntry_t=None)

# def mFll_Stt_fe(laDir_s=None, laSortKey_cll=lambda _el: _el.name.upper(),
#                      laChe_b:bool=False) -> bool:
#   if laDir_s is None: laDir_s = os.curdir # Init|RScan
  
#   if mStt_d['kRtDir_s'] is None: loDir_s = os.path.realpath(laDir_s)
#   else:
#     loDir_s = os.path.realpath(os.path.join(mStt_d['kRtDir_s'], mStt_d['kCurRelDir_s'], laDir_s))
#     if laChe_b:
#       loCommPrx_s = os.path.commonpath((mStt_d['kRtDir_s'], loDir_s)) # 2Do Cch:ValueError
#       if loCommPrx_s != mStt_d['kRtDir_s']: # Sec: loDir_s is not SbDir(mStt_d['kRtDir_s'])
#         print("DVL:loDir_s is not SbDir(mStt_d['kRtDir_s'])")
#         return False
  
#   # if os.path.exists(loDir_s) and os.path.isdir(loDir_s): # Dlg(scandir)
#   if laSortKey_cll is None:
#     mStt_d['kDirEntry_t'] = tuple(os.scandir(loDir_s))
#   else:
#     mStt_d['kDirEntry_t'] = tuple(sorted(os.scandir(loDir_s), key=laSortKey_cll))
#   if mStt_d['kRtDir_s'] is None:
#     mStt_d['kRtDir_s'] = loDir_s
#     mStt_d['kCurRelDir_s'] = os.curdir
#   else: 
#     mStt_d['kCurRelDir_s'] = os.path.relpath(loDir_s, start=mStt_d['kRtDir_s'])
#   return True
#   # else: return False

mStt_d = dict(kStkDir_l=[], kDirEntry_t=None, kTSum_t=None)
# mStt_d = dict(kStkDir_llist[str]=[], kDirEntry_t:tuple[os.DirEntry]=None)

def mFll_Stt_fe(laNewDir_s=None, laSortKey_cll=lambda _el: _el.name.upper(),
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

  if laScan_b or mStt_d['kDirEntry_t'] is None or mStt_d['kTSum_t'] is None:
    # print(f'DVL:{laScan_b=}')
    if callable(laSortKey_cll):
      mStt_d['kDirEntry_t'] = tuple(sorted(os.scandir(loDir_s), key=laSortKey_cll))
    else:
      mStt_d['kDirEntry_t'] = tuple(os.scandir(loDir_s))
    loTT_t = tuple((_el.name, _el.is_file(follow_symlinks=False), _el.is_dir(follow_symlinks=False),
        _el.is_symlink()) for _el in mStt_d['kDirEntry_t'])
    mStt_d['kTSum_t'] = (sum(_el[1] for _el in loTT_t), sum(_el[2] for _el in loTT_t),
        sum(_el[3] for _el in loTT_t))

def mOuP_Stt_fmp(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  lo_s = "ТекДиректория:({}), "
  if mStt_d['kDirEntry_t'] is None: lo_s = lo_s.format('')
  else: lo_s = lo_s.format(mStt_d['kStkDir_l'][-1])
  if mStt_d['kDirEntry_t'] is None:
    lo_s += f"All:0"
  elif mStt_d['kTSum_t'] is None:
    lo_s += f"All:{len(mStt_d['kDirEntry_t'])}"
  else:
    lo_s += (f"(All,File,Dir,SLink):({len(mStt_d['kDirEntry_t'])}," +
       ','.join(str(_el) for _el in mStt_d['kTSum_t']) + ')')
  # print(f"kRtDir_s={mStt_d['kRtDir_s']}, kCurRelDir_s={mStt_d['kCurRelDir_s']}",
  #     lo_s, sep=', ', file=file)
  # tNL_s = '\n'
  # print(f"{tNL_s.join((str(_el) for _el in mStt_d['kDirEntry_t']))}")
  # print(tNL_s.join((str(_el) for _el in mStt_d['kDirEntry_t'])))
  print(lo_s, file=file)

# InPHstEl:(fCurDirL_ix, fInP_s, fDesc_s, fRes_a)

def mA_Exit_fm(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  laSf_o.fRunLoop_b = False


# InfoMenuItems
def mA_SysInfo_ffmp(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  loMsg_s = f"{sys.platform=}\n{sys.version=}\n{sys.api_version=}."
  print(loMsg_s, file=file)
  return loMsg_s
def mA_MyInfo_ffmp(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  loMsg_s = "Creator/Author: Mike Vl. Vlasov <dev.mikevvl@outlook.com>."
  print(loMsg_s, file=file)
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

def mA_VieAll_fm(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  loAll_i = sum(mStt_d['kTSum_t'])
  lo_s = f" in Dir:({mStt_d['kStkDir_l'][-1]})"
  if loAll_i == 0:
    print("No files, directories or softlinks" + lo_s + '.', file=file)
  elif (loCo_i:=mStt_d['kTSum_t'][0]) != 0: #file|files
    lo_s = str(loCo_i) + ' file' if loCo_i == 1 else ' files' + lo_s + ':\n'
    print(str(loCo_i) + ' file' if loCo_i == 1 else ' files' + lo_s + ':', file=file)
    print(*(_el.name for _el in mStt_d['kDirEntry_t']
    if _el.is_file(follow_symlinks=False)), sep='\n', file=file)
  elif mStt_d['kTSum_t'][1] != 0: #directory|directories
    pass
  elif mStt_d['kTSum_t'][2] != 0: #softlink|softlinks
    pass
  return

def mA_CreFi_fm(laSf_o:mMenu_c, file:mSupportsWrite_ca=sys.stdout):
  return

# mStt_d = dict(kStkDir_l=[], kDirEntry_t=None, kTSum_t=None)
mMainMenu_d = {
 '0': ('Создать файл', None, None), # open(Na, mode='x)
 '1': ('Создать папку', None),
 '2': ('Удалить файл', None),
 '3': ('Удалить папку', None),
 '4': ('Копировать файл', None),
 '5': ('Копировать папку', None),
 '6': ('Просмотр содержимого рабочей директории', None),
 '7': ('Посмотреть только папки', None),
 '8': ('Посмотреть только файлы', None),
 '9': ('Смена рабочей директории', None),
 'В': ('Играть в викторину', mA_victory_ffmp),
 'Б': ('Мой банковский счет', mA_MyBankAcc_ffmp),
 'И': ('Просмотр информации об операционной системе', mA_SysInfo_ffmp),
 'Я': ('Создатель программы', mA_MyInfo_ffmp, None),
 'Ы': ('Выход', mA_Exit_fm),
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
