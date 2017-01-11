var utils = {
  translate: function(word) {
    const indonesianDictionary = {
      pendidikan: 'education',
      demografi: 'demographics',
      agama: 'religion',
      pekerjaan: 'occupation',
      pernikahan: 'marriage'
    }
    const englishDictionary = {
      education: 'pendidikan',
      demographics: 'demografi',
      religion: 'agama',
      occupation: 'pekerjaan',
      marriage: 'pernikahan'
    }
    return indonesianDictionary[word] ? 
           indonesianDictionary[word] : englishDictionary[word];
  },
  regionList: ['cakung', 'cempaka putih', 'cengkareng', 'cilandak', 
               'cilincing', 'cipayung', 'ciracas', 'duren sawit', 
               'gambir', 'grogol petamburan', 'jagakarsa', 'jatinegara', 
               'johar baru', 'kalideres', 'kebayoran baru', 
               'kebayoran lama', 'kebon jeruk', 'kelapa gading', 
               'kemayoran', 'kembangan', 'koja', 'kramat jati', 
               'makasar', 'mampang prapatan', 'matraman', 'menteng', 
               'pademangan', 'palmerah', 'pancoran', 'pasar minggu', 
               'pasar rebo', 'penjaringan', 'pesanggrahan', 
               'pulo gadung', 'sawah besar', 'senen', 'setiabudi', 
               'taman sari', 'tambora', 'tanah abang', 'tanjung priok', 
               'tebet'],
  getKeys: function() {
    Object.keys(this).filter((key) => key != "getKeys")
                     .map((key) => {console.log(key);})
  },
  getColorPalette: function(numColors) {
    const bgColors = [
      'rgba(255, 131, 131, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(255, 206, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)',
      'rgba(153, 102, 255, 0.2)',
      'rgba(255, 159, 64, 0.2)',
      'rgba(99, 234, 255, 0.2)',
      'rgba(252, 110, 63, 0.2)',
      'rgba(79, 247, 135, 0.2)',
      'rgba(96, 120, 255, 0.2)',
    ];
    const borderColors = [
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
    ];
    const paletteSize = 10;

    return {
      background: Array(numColors).fill('')
                                  .map((elem, index) => 
                                       bgColors[index % paletteSize]),
      border: Array(numColors).fill('')
                              .map((elem, index) => 
                                   borderColors[index % paletteSize])
    }
  }  
}

module.exports = utils;