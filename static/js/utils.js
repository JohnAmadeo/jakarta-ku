class Utils {
  constructor() {
    this.initializeDictionary = this.initializeDictionary.bind(this);
    this.getDataList = this.getDataList.bind(this);
    this.getPalette = this.getPalette.bind(this);
    this.translate = this.translate.bind(this);
    this.dict = this.initializeDictionary();
    this.translations = this.initializeTranslations();
  }
  initializeTranslations() {
    let translations = {
      'pendidikan': 'education',
      'demografi' : 'demographics',
      'agama'     : 'religion',
      'pekerjaan' : 'occupation',
      'pernikahan': 'marriage'
    };

    return translations;
  }
  initializeDictionary() {
    let dict = {};

    dict.category = [
      'pendidikan',
      'demografi' ,
      'agama'     ,
      'pekerjaan' ,
      'pernikahan'
    ]  

    dict.region = [
      'cakung', 'cempaka putih', 'cengkareng', 'cilandak', 'cilincing', 
      'cipayung', 'ciracas', 'duren sawit', 'gambir', 
      'grogol petamburan', 'jagakarsa', 'jatinegara', 'johar baru', 
      'kalideres', 'kebayoran baru', 'kebayoran lama', 'kebon jeruk', 
      'kelapa gading', 'kemayoran', 'kembangan', 'koja', 'kramat jati', 
      'makasar', 'mampang prapatan', 'matraman', 'menteng', 
      'pademangan', 'palmerah', 'pancoran', 'pasar minggu', 
      'pasar rebo', 'penjaringan', 'pesanggrahan', 'pulo gadung', 
      'sawah besar', 'senen', 'setiabudi', 'taman sari', 'tambora', 
      'tanah abang', 'tanjung priok', 'tebet'
    ];

    dict.palette = {
      background: [
        'rgba(255, 131, 131, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(99, 234, 255, 0.2)',
        'rgba(252, 110, 63, 0.2)',
        'rgba(79, 247, 135, 0.2)',
        'rgba(96, 120, 255, 0.2)'
      ],
      border: [
        'rgba(255,131,131,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(99, 234, 255, 1)',
        'rgba(252, 110, 63, 1)',
        'rgba(79, 247, 135, 1)',
        'rgba(96, 120, 255, 1)',
      ]
    }

    dict.religion = [
      'islam',
      'kristen',
      'katholik',
      'hindu',
      'budha',
      'khonghuchu'
    ];

    dict.education = [
      'tidak/belum sekolah',
      'tidak/belum tamat sd',
      'sd',
      'smp',
      'sma',
      'd1/d2',
      'd3',
      's1/d4',
      's2',
      's3'
    ];

    dict.marriage = [
      'belum kawin', 
      'kawin',
      'cerai hidup',
      'cerai mati' 
    ];

    dict.demographics = [ 
      '0-4 laki-laki',
      '0-4 perempuan',
      '5-9 laki-laki',
      '5-9 perempuan',
      '10-14 laki-laki',
      '10-14 perempuan',
      '15-19 laki-laki',
      '15-19 perempuan',
      '20-24 laki-laki',
      '20-24 perempuan',
      '25-29 laki-laki',
      '25-29 perempuan',
      '30-34 laki-laki',
      '30-34 perempuan',
      '35-39 laki-laki',
      '35-39 perempuan',
      '40-44 laki-laki',
      '40-44 perempuan',
      '45-49 laki-laki',
      '45-49 perempuan',
      '50-54 laki-laki',
      '50-54 perempuan',
      '55-59 laki-laki',
      '55-59 perempuan',
      '60-64 laki-laki',
      '60-64 perempuan',
      '65-69 laki-laki',
      '65-69 perempuan',
      '70-74 laki-laki',
      '70-74 perempuan',
      '>75 laki-laki',
      '>75  perempuan' 
    ];

    dict.occupation = [ 
      'akuntan',
      'anggota bpk',
      'anggota dpd',
      'anggota dpr-ri',
      'anggota dprd kabupaten/kota',
      'anggota dprd provinsi',
      'anggota kabinet/kementerian',
      'anggota mahkamah konstitusi',
      'apoteker',
      'arsitek',
      'belum/tidak bekerja',
      'biarawati',
      'bidan',
      'bupati',
      'buruh harian lepas',
      'buruh nelayan/perikanan',
      'buruh peternakan',
      'buruh tani/perkebunan',
      'dokter',
      'dosen',
      'duta besar',
      'gubernur',
      'guru',
      'imam mesjid',
      'industri',
      'juru masak',
      'karyawan bumd',
      'karyawan bumn',
      'karyawan honorer',
      'karyawan swasta',
      'kepala desa',
      'kepolisian ri',
      'konstruksi',
      'konsultan',
      'lainnya',
      'mekanik',
      'mengurus rumah tangga',
      'nelayan/perikanan',
      'notaris',
      'paraji',
      'paranormal',
      'pastor',
      'pedagang',
      'pegawai negeri sipil',
      'pelajar/mahasiswa',
      'pelaut',
      'pembantu rumah tangga',
      'penata busana',
      'penata rambut',
      'penata rias',
      'pendeta',
      'peneliti',
      'pengacara',
      'pensiunan',
      'penterjemah',
      'penyiar radio',
      'penyiar televisi',
      'perancang busana',
      'perangkat desa',
      'perawat',
      'perdagangan',
      'petani/pekebun/peternak',
      'pialang',
      'pilot',
      'promotor acara',
      'psikiater/psikolog',
      'seniman',
      'sopir',
      'tabib',
      'tentara nasional indonesia',
      'transportasi',
      'tukang batu',
      'tukang cukur',
      'tukang gigi',
      'tukang jahit',
      'tukang kayu',
      'tukang las/pandai besi',
      'tukang listrik',
      'tukang sol sepatu',
      'ustadz/mubaligh',
      'wakil gubernur',
      'wakil presiden',
      'walikota',
      'wartawan',
      'wiraswasta' 
    ];

    return dict;
  }
  
  translate(word) {
    return this.translations[word];
  }

  getDataList(list_type) {
    return this.dict[list_type];
  }
  
  getPalette(numColors, startColor) {
    const backgroundColors = this.dict.palette.background;
    const borderColors = this.dict.palette.border;
    const paletteSize = backgroundColors.length;
    const offset = backgroundColors.indexOf(startColor);

    return {
      background: Array(numColors)
                  .fill('')
                  .map((elem, index) => 
                       backgroundColors[(index + offset) % paletteSize]),
      border: Array(numColors)
              .fill('')
              .map((elem, index) => 
                    borderColors[(index + offset) % paletteSize])
    }
  }  

  getLabel(label, category, language_code) {
    const index = dict[category]['IDN'].indexOf(label.toLowerCase());
    return dict[category][language_code][index];
  }
}

module.exports = Utils;