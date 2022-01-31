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
import os, shutil, sys
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

tDig_l = ['Создать файл', 'Создать папку', 'Удалить файл', 'Удалить папку',
 'Копировать файл', 'Копировать папку', 'Просмотр содержимого рабочей директории',
 'Посмотреть только папки', 'Посмотреть только файлы']
tAlpha_l = [ 'Просмотр информации об операционной системе',
 'Создатель программы', 'Играть в викторину', 'Мой банковский счет',
 'Смена рабочей директории', 'Выход']
# t_d = dict(**dict((str(_i), [_s, None]) for _i, _s in enumerate(tDig_l, 1)),
#     **dict((_s1, [_s, None]) for _s1, _s in zip('ИЯВБСЫ', tAlpha_l)))
tMenu_l = list((str(_i), [_s, None]) for _i, _s in enumerate(tDig_l, 1))
tMenu_d = dict(tMenu_l + list((_s1, [_s, None])
    for _s1, _s in zip('ИЯВБСЫ', tAlpha_l)))
 
tInnStt_d = dict(kRtDir_s=None, kCurDir_s=None, kDirEntry_t=None)
# InPHstEl:(fCurDirL_ix, fInP_s, fDesc_s, fRes_a)

def tVieHst_ffp(laSf_o, file=sys.stdout):
  print(f"История покупок (всего {len(laSf_o.fInnStt_d['kBuyHstT_l'])} зап.):",
      *enumerate(laSf_o.fInnStt_d['kBuyHstT_l'], 1), '', sep='\n', file=file)
  return (laSf_o.fInnStt_d['kAccSum_n'], len(laSf_o.fInnStt_d['kBuyHstT_l']))

def tExit_f(laSf_o, file=sys.stdout):
  laSf_o.fRunLoop_b = False

def tSysInfo_ffp(laSf_o, file=sys.stdout):
  loMsg_s = f"{sys.platform=}\n{sys.version=}\n{sys.api_version=}."
  print(loMsg_s, file=file)
  return loMsg_s
def tMyInfo_ffp(laSf_o, file=sys.stdout):
  loMsg_s = "Creator/Author: Mike Vl. Vlasov <dev.mikevvl@outlook.com>."
  print(loMsg_s, file=file)
  return loMsg_s
def tvictory_ffp(laSf_o, file=sys.stdout):
  return mod.victory.main(None)
def tMyBankAcc_ffp(laSf_o, file=sys.stdout):
  return mod.MyBankAcc.main(None, fFile_o=file)


tMenu_d = {'1': ['Создать файл', None],
 '2': ['Создать папку', None],
 '3': ['Удалить файл', None],
 '4': ['Удалить папку', None],
 '5': ['Копировать файл', None],
 '6': ['Копировать папку', None],
 '7': ['Просмотр содержимого рабочей директории', None],
 '8': ['Посмотреть только папки', None],
 '9': ['Посмотреть только файлы', None],
 'С': ['Смена рабочей директории', None],
 'И': ['Просмотр информации об операционной системе', tSysInfo_ffp],
 'В': ['Играть в викторину', tvictory_ffp],
 'Б': ['Мой банковский счет', tMyBankAcc_ffp],
 'Я': ['Создатель программы', tMyInfo_ffp],
 'Ы': ['Выход', tExit_f]}

def prn_InnStt_fp(laSf_o, laInnStt_d, file=sys.stdout):
  # 2Do: CheExs(kAccSum_n, kBuyHstT_l)
  # if 'kAccSum_n' in laInnStt_d and 'kBuyHstT_l' in laInnStt_d:
  loNone_b = laInnStt_d['kDirEntry_t'] is None
  lo_s = f"kDirEntry_t=None" if loNone_b else f"{len(laInnStt_d['kDirEntry_t'])=}"
  loNone_b = laInnStt_d['kActHst_l'] is None
  lo_s += f", kActHst_l=None" if loNone_b else f", {len(laInnStt_d['kActHst_l'])=}"
  print(f"kRtDir_s={laInnStt_d['kRtDir_s']}, kCurDir_s={laInnStt_d['kCurDir_s']}",
      lo_s, sep=', ', file=file)

def main(laArgs: list[str], *laArg_l, **laKwArg_d) -> dict:
  # Ww:laArgs(sys.argv[1:])
  loKwArg_d = dict(fInnStt_d=tInnStt_d, fPrnInnStt_cll=prn_InnStt_fp,
      fHeaFmt_s= mod.MVVlStd.glSep_s + '\nКонсольный файловый менеджер:')
  loKwArg_d.update(laKwArg_d)
  tMenu_o = mod.MVVlStd.Menu_c(tMenu_d, **loKwArg_d)
  # mod.victory.main(None)
  # tRes_d = mod.MyBankAcc.main(None, fFile_o=sys.stdout)
  tRes_d = tMenu_o()
  print(tRes_d)
  return tRes_d
  # t_l = mod.MVVlStd.glStdMsg4InP_l[:]
  # t_l[0] = 'Выберите'
  # print(t_l[0], mod.MVVlStd.glStdMsg4InP_l[0])
  # print(mod.MVVlStd.inp_FltAVali_fefi(' пункт меню'))

if __name__ == '__main__':
    # import sys
    # main(sys.argv[1:])
    print(sys.executable, *sys.argv, sep='\n')
    # print('', *sys.orig_argv, sep='\n')
    main(None)
