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

t_l = ['Создать папку', 'Удалить файл', 'Удалить папку', 'Копировать файл',
 'Копировать папку', 'Просмотр содержимого рабочей директории',
 'Посмотреть только папки', 'Посмотреть только файлы',
 'Просмотр информации об операционной системе', 'Создатель программы',
 'Играть в викторину', 'Мой банковский счет', 'Смена рабочей директории',
 'Выход']
tInnStt_d = dict(kRtDir_s=None, kCurDir_s=None, kDirEntry_t=None)
# InPHstEl:(fCurDirL_ix, fInP_s, fDesc_s, fRes_a)

def tExit_fm(self, file=sys.stdout):
  self.IsRun_b = False

# tMenu_d = {'1':('Пополнение счета', tRefillAcc_fm, ??Type??(Exit, Back, SbMenu, CtrlVieMenu??)),
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

def main(laArgs: list[str]) -> None:
  # mod.victory.main(None)
  tRes_d = mod.MyBankAcc.main(None)
  print(tRes_d)
  # t_l = mod.MVVlStd.glStdMsg4InP_l[:]
  # t_l[0] = 'Выберите'
  # print(t_l[0], mod.MVVlStd.glStdMsg4InP_l[0])
  # print(mod.MVVlStd.inp_FltAVali_fefi(' пункт меню'))

if __name__ == '__main__':
    # import sys
    # main(sys.argv[1:])
    main(None)
