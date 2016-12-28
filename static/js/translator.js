var translator = {
  indoToEnglish: function(word) {
    const dictionary = {
      pendidikan: 'education',
      demografi: 'demographics',
      agama: 'religion',
      pekerjaan: 'occupation',
      pernikahan: 'marriage'
    }
    return dictionary[word];
  },
  englishToIndo: function(word) {
    const dictionary = {
      education: 'pendidikan',
      demographics: 'demografi',
      religion: 'agama',
      occupation: 'pekerjaan',
      marriage: 'pernikahan'
    }
    return dictionary[word];    
  }
}

module.exports = translator;