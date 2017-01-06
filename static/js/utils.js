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
               'tebet'],
  getKeys: function() {
    Object.keys(this).filter((key) => key != "getKeys")
                     .map((key) => {console.log(key);})
  },
  getColorPalette: function(num_colors) {
    const bg_colors = [
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
    const border_colors = [
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

    return Array(num_colors).fill('')
                   .map(function(elem, index) {
                    return {
                      background: bg_colors[index % num_colors],
                      border: border_colors[index % num_colors]
                    }
                   });
  }  
}

module.exports = utils;