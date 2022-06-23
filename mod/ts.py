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
  fAFile4Prn_o: object = sys.stdout

  def __post_init__(self):
    self.fMenuItm_d = dict(self.fMenuItm_d)
    if self.fOutStt_d is not None:
      self.fOutStt_d = copy.deepcopy(dict(self.fOutStt_d))
      if self.fPrnOutStt_cll is None:
        self.fPrnOutStt_cll = lambda sf_o, laStt_d, file=self.fAFile4Prn_o: print(laStt_d, file=file)
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

  # 2Do: MaB: oup_fmp(self, file=fAFile4Prn_o)
  # 2Do: MaB Onl(9+KeyExit OR Fit2Scr+KeyExit) w/Set(sf.WhiVieItmKey_l)
  def prn_fmp(self, file=fAFile4Prn_o):
    if bool(self.fMenuItm_d):
      if self.fHeaFmt_s != '': print(self.fHeaFmt_s, file=file)
      print(*(self.fItmFmt_s.format(_k=_k, _v=self[_k]) for _k in self),
          sep='\n', file=file)
      self.prn_Info_fmp(file=file)
      if self.fFooFmt_s != '': print(self.fFooFmt_s, file=file)

  # def __str__(self):; __format__; tVieHst_fmp
  def prn_Info_fmp(self, file=fAFile4Prn_o):
    if self.fPrnOutStt_cll and callable(self.fPrnOutStt_cll):
      self.fPrnOutStt_cll(self, laStt_d=self.fOutStt_d, file=file)

  # def add_Itms?_ffm(self):
  # def del_Itms?_ffpm(self):
  # def get_Keys?_ffpm(self):

  # def run_ffpm(self):
  def __call__(self, file=fAFile4Prn_o): # MainLoop
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
