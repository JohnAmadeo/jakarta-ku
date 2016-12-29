var utils = {
  translate: function(word) {
    const indonesian_dictionary = {
      pendidikan: 'education',
      demografi: 'demographics',
      agama: 'religion',
      pekerjaan: 'occupation',
      pernikahan: 'marriage'
    }
    const english_dictionary = {
      education: 'pendidikan',
      demographics: 'demografi',
      religion: 'agama',
      occupation: 'pekerjaan',
      marriage: 'pernikahan'
    }
    return indonesian_dictionary[word] ? indonesian_dictionary[word] :
                                         english_dictionary[word];
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
               'tebet']
}

module.exports = utils;