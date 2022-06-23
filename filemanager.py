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
import mod.MVVlStd, mod.victory, mod.MyBankAcc

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

mDig_l = ['Создать файл', 'Создать папку', 'Удалить файл', 'Удалить папку',
 'Копировать файл', 'Копировать папку', 'Про1смотр содержимого рабочей директории',
 'Посмотреть только папки', 'Посмотреть только файлы']
mAlpha_l = [ 'Просмотр информации об операционной системе',
 'Создатель программы', 'Играть в викторину', 'Мой банковский счет',
 'Смена рабочей директории', 'Выход']
# t_d = dict(**dict((str(_i), [_s, None]) for _i, _s in enumerate(mDig_l, 1)),
#     **dict((_s1, [_s, None]) for _s1, _s in zip('ИЯВБСЫ', mAlpha_l)))
mMenu_l = list((str(_i), [_s, None]) for _i, _s in enumerate(mDig_l, 1))
mMenu_d = dict(list((str(_i), [_s, None]) for _i, _s in enumerate(mDig_l, 1))
             + list((_s1, [_s, None]) for _s1, _s in zip('ИЯВБСЫ', mAlpha_l)))
 
mStt_d = dict(kRtDir_s=None, kCurRelDir_s=None, kDirEntry_t=None)

def mFll_Stt_ff(laDir_s=None, laSortKey_cll=lambda _el: _el.name.upper()) -> bool:
  if laDir_s is None: laDir_s = os.curdir # Init|RScan
  
  if mStt_d['kRtDir_s'] is None: loDir_s = os.path.realpath(laDir_s)
  else:
    loDir_s = os.path.realpath(os.path.join(mStt_d['kRtDir_s'], mStt_d['kCurRelDir_s'], laDir_s))
    loCommPrx_s = os.path.commonpath((mStt_d['kRtDir_s'], loDir_s)) # 2Do Cch:ValueError
    if loCommPrx_s != mStt_d['kRtDir_s']: # Sec: loDir_s is not SbDir(mStt_d['kRtDir_s'])
      return False
  
  # if os.path.exists(loDir_s) and os.path.isdir(loDir_s): # Dlg(scandir)
  if laSortKey_cll is None:
    mStt_d['kDirEntry_t'] = tuple(os.scandir(loDir_s))
  else:
    mStt_d['kDirEntry_t'] = tuple(sorted(os.scandir(loDir_s), key=laSortKey_cll))
  if mStt_d['kRtDir_s'] is None:
    mStt_d['kRtDir_s'] = loDir_s
    mStt_d['kCurRelDir_s'] = os.curdir
  else: 
    mStt_d['kCurRelDir_s'] = os.path.relpath(loDir_s, start=mStt_d['kRtDir_s'])
  return True
  # else: return False

# InPHstEl:(fCurDirL_ix, fInP_s, fDesc_s, fRes_a)

def mA_Exit_fm(laSf_o:mod.MVVlStd.mMenu_ca,
    file:mod.MVVlStd.mSupportsWrite_ca=sys.stdout):
  laSf_o.fRunLoop_b = False

def mA_SysInfo_ffmp(laSf_o:mod.MVVlStd.mMenu_ca,
    file:mod.MVVlStd.mSupportsWrite_ca=sys.stdout):
  loMsg_s = f"{sys.platform=}\n{sys.version=}\n{sys.api_version=}."
  print(loMsg_s, file=file)
  return loMsg_s
def mA_MyInfo_ffmp(laSf_o:mod.MVVlStd.mMenu_ca, file:mod.MVVlStd.mSupportsWrite_ca=sys.stdout):
  loMsg_s = "Creator/Author: Mike Vl. Vlasov <dev.mikevvl@outlook.com>."
  print(loMsg_s, file=file)
  return loMsg_s

def mA_victory_ffmp(laSf_o:mod.MVVlStd.mMenu_ca, file:mod.MVVlStd.mSupportsWrite_ca=sys.stdout):
  return mod.victory.main(None)
def mA_MyBankAcc_ffmp(laSf_o:mod.MVVlStd.mMenu_ca, file:mod.MVVlStd.mSupportsWrite_ca=sys.stdout):
  return mod.MyBankAcc.main(None, fAFile4Prn_o=file)

# def mA_VieHst_ffmp(laSf_o, file:mod.MVVlStd.mSupportsWrite_ca=sys.stdout):
#   print(f"История покупок (всего {len(laSf_o.fOutStt_d['kBuyHstT_l'])} зап.):",
#       *enumerate(laSf_o.fOutStt_d['kBuyHstT_l'], 1), '', sep='\n', file=file)
#   return (laSf_o.fOutStt_d['kAccSum_n'], len(laSf_o.fOutStt_d['kBuyHstT_l']))
#   laSf_o.fInP_s, laSf_o.fInP_k

mMenu_d = {'1': ('Создать файл', None, None),
 '2': ('Создать папку', None),
 '3': ('Удалить файл', None),
 '4': ('Удалить папку', None),
 '5': ('Копировать файл', None),
 '6': ('Копировать папку', None),
 '7': ('Просмотр содержимого рабочей директории', None),
 '8': ('Посмотреть только папки', None),
 '9': ('Посмотреть только файлы', None),
 'С': ('Смена рабочей директории', None),
 'В': ('Играть в викторину', mA_victory_ffmp),
 'Б': ('Мой банковский счет', mA_MyBankAcc_ffmp),
 'И': ('Просмотр информации об операционной системе', mA_SysInfo_ffmp),
 'Я': ('Создатель программы', mA_MyInfo_ffmp, None),
 'Ы': ('Выход', mA_Exit_fm)}

def mOuP_Stt_fmp(laSf_o:mod.MVVlStd.mMenu_c,
    file:mod.MVVlStd.mSupportsWrite_ca=sys.stdout):
  loNone_b = mStt_d['kDirEntry_t'] is None
  lo_s = f"kDirEntry_t=None" if loNone_b else f"{len(mStt_d['kDirEntry_t'])=}"
  print(f"kRtDir_s={mStt_d['kRtDir_s']}, kCurRelDir_s={mStt_d['kCurRelDir_s']}",
      lo_s, sep=', ', file=file)

def main(laArgs: list[str], *laArg_l, **laKwArg_d) -> dict:
  ''' Arg laKMenuCrePP_d=dict(BasePP 4 Cre All Menu In2(Sf))
  '''
  # Ww:laArgs(sys.argv[1:])
  if 'laKMenuCrePP_d' in laKwArg_d:
    loKwArg_d = copy.deepcopy(dict(laKwArg_d['laKMenuCrePP_d']))
  else: loKwArg_d = {}
  loAppDesc_s = 'Консольный файловый менеджер'
  loKwArg_d.update(dict(fPrnOutStt_cll=mOuP_Stt_fmp,
      fAppTtl_s=loAppDesc_s))
  loMenu_o = mod.MVVlStd.mMenu_c(mMenu_d, **loKwArg_d)
  # mod.victory.main(None)
  # loRes_o = mod.MyBankAcc.main(None, fAFile4Prn_o=sys.stdout)
  loRes_o = loMenu_o()
  print(loRes_o) #DVL
  return loRes_o
  # t_l = mod.MVVlStd.glStdMsg4InP_l[:]
  # t_l[0] = 'Выберите'
  # print(t_l[0], mod.MVVlStd.glStdMsg4InP_l[0])
  # print(mod.MVVlStd.mInP_FltAVali_fefi(' пункт меню'))

if __name__ == '__main__':
    # import sys
    # main(sys.argv[1:])
    # print(sys.executable, *sys.argv, sep='\n')
    # print('', *sys.orig_argv, sep='\n')
    main(None)
