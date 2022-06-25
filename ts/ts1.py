@dataclass
class Menu_c():

  fOutMenuItm_d: dict = field(default_factory=dict) # OutVar: ItmFmt(_k=Key, _v=[Desc_s, _cll, ??Type_en:(AlwOut, ...)])
  # fOutStt_d: dict = None # OutVar
  fAppTtl_s: str = ''
  fPrnOutStt_cll: Callable = None # OutVar # [self, file]; ??(Slv:NN)Df: IF fOutStt_d is !None -> print(fOutStt_d)
  fIterSortKey_cll: Callable = None # [key] ??(Prop4Set): AsIn2fOutMenuItm_d OR (lambda _el: str(_el))|int
  fHeaFmt_s: str = None
  fFooFmt_s: str = None
  fItmFmt_s: str = '{_k!s:>2}. {_v[0]}'
  fActHst_l: list = field(default_factory=list)
  # 2Do: PP(Max(Col|Row)) 4 prn_fmp
  fAFile4Prn_o: object = sys.stdout

  def __post_init__(self):
    if self.fHeaFmt_s is not None: self.fHeaFmt_s = str(self.fHeaFmt_s)
    else:
      self.fHeaFmt_s = glSep_s
      if self.fAppTtl_s: self.fHeaFmt_s += f'\n{self.fAppTtl_s}:'
    if self.fFooFmt_s is not None: self.fFooFmt_s = str(self.fFooFmt_s)
    else: self.fFooFmt_s = glSep_s[:len(glSep_s)//3 *2]
    
    self.fRunLoop_b = bool(self.fOutMenuItm_d)
    self.fInP_s, self.fInP_k = None, None
    if self.fActHst_l is not None:
      self.fActHst_l.append((time.time_ns(), 'Inn', '__post_init__', True))

  def __iter__(self): # 2Do: MaB Onl WhiUse(prn_fmp)
    if self.fIterSortKey_cll is None:
      return (_k for _k in self.fOutMenuItm_d.keys())
    return (_k for _k in sorted(self.fOutMenuItm_d.keys(), key=self.fIterSortKey_cll))

  def __getitem__(self, key): # BOf:KISS
    return self.fOutMenuItm_d[key]

  def __len__(self): # BOf:KISS
    return len(self.fOutMenuItm_d)

  def __contains__(self, key): # BOf:KISS
    return key in self.fOutMenuItm_d

  # 2Do: MaB: oup_fmp(self, file=fAFile4Prn_o)
  # 2Do: MaB Onl(9+KeyExit OR Fit2Scr+KeyExit) w/Set(sf.WhiVieItmKey_l)
  def prn_fmp(self, file=fAFile4Prn_o):
    if bool(self.fOutMenuItm_d):
      if self.fHeaFmt_s != '': print(self.fHeaFmt_s, file=file)
      print(*(self.fItmFmt_s.format(_k=_k, _v=self[_k]) for _k in self),
          sep='\n', file=file)
      self.prn_Info_fmp(file=file)
      if self.fFooFmt_s != '': print(self.fFooFmt_s, file=file)

  # 2Do: __str__(self), __format__, tVieHst_fmp
  def prn_Info_fmp(self, file=fAFile4Prn_o):
    if self.fPrnOutStt_cll and callable(self.fPrnOutStt_cll):
      self.fPrnOutStt_cll(self, file=file)

  # 2Do: add_Itms?_ffm(self), del_Itms?_ffpm(self), def get_Keys?_ffpm(self):
  # ??run_ffpm(self):
  def __call__(self, file=fAFile4Prn_o): # MainLoop
    if self.fActHst_l is not None:
      self.fActHst_l.append((time.time_ns(), 'Inn', 'Beg:MainLoop', True))
    while self.fRunLoop_b:
      self.prn_fmp(file=file)
      self.fInP_s, self.fInP_k = None, None # ??&| In2__post_init__
      self.fInP_s = inp_FltAVali_fefi(f' пункт меню', laInPTypeFlt_cll=None,
          file=file)[0].strip()
      if self.fInP_s in self:
        self.fInP_k = self.fInP_s
      else:
        try: self.fInP_k = int(self.fInP_s)
        except ValueError as le_o: self.fInP_k = None
        else:
          if self.fInP_k not in self: self.fInP_k = None
      if self.fInP_k is not None:
        lo_cll = self[self.fInP_k][1]
        if lo_cll is None: # 2Do:??AddHst
          print(f'DVL: None 4 calling Fu() пункт меню({self.fInP_k})', file=file)
          continue
        else:
          loRes_a = lo_cll(self, file=file)
          if self.fActHst_l is not None:
            self.fActHst_l.append((time.time_ns(), 'InP',
                f'({self.fInP_s})' + self[self.fInP_k][0], loRes_a))
      else:
          print(f'MSG: Неверный пункт меню({self.fInP_s})', file=file) # 2Do:??AddHst
    else:
      if self.fHeaFmt_s != '': print(self.fHeaFmt_s, file=file)
      print('До свидания!', file=file)
      if self.fActHst_l is not None:
        self.fActHst_l.append((time.time_ns(), 'Inn', 'End:MainLoop', True))
      if self.fFooFmt_s != '': print(self.fFooFmt_s, file=file)

    return self.fActHst_l
