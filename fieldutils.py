def get_field_display_order(category, field):
    education_list = \
    {
        "Tidak/Belum Sekolah": 1, "Tidak/Belum Tamat SD": 2, "SD": 3, 
        "SMP": 4, "SMA": 5, "D1/D2": 6, "D3": 7, "S1/D4": 8, "S2": 9, 
        "S3": 10
    }
    occupation_list = \
    {
        "Akuntan": 0,
        "Anggota BPK": 1,
        "Anggota DPD": 2,
        "Anggota DPR-RI": 3,
        "Anggota DPRD Kabupaten/Kota": 4,
        "Anggota DPRD Provinsi": 5,
        "Anggota Kabinet/Kementerian": 6,
        "Anggota Mahkamah Konstitusi": 7,
        "Apoteker": 8,
        "Arsitek": 9,
        "Belum/Tidak Bekerja": 10,
        "Biarawati": 11,
        "Bidan": 12,
        "Bupati": 13,
        "Buruh Harian Lepas": 14,
        "Buruh Nelayan/Perikanan": 15,
        "Buruh Peternakan": 16,
        "Buruh Tani/Perkebunan": 17,
        "Dokter": 18,
        "Dosen": 19,
        "Duta Besar": 20,
        "Gubernur": 21,
        "Guru": 22,
        "Imam Mesjid": 23,
        "Industri": 24,
        "Juru Masak": 25,
        "Karyawan BUMD": 26,
        "Karyawan BUMN": 27,
        "Karyawan Honorer": 28,
        "Karyawan Swasta": 29,
        "Kepala Desa": 30,
        "Kepolisian RI": 31,
        "Konstruksi": 32,
        "Konsultan": 33,
        "Lainnya": 34,
        "Mekanik": 35,
        "Mengurus Rumah Tangga": 36,
        "Nelayan/Perikanan": 37,
        "Notaris": 38,
        "Paraji": 39,
        "Paranormal": 40,
        "Pastor": 41,
        "Pedagang": 42,
        "Pegawai Negeri Sipil": 43,
        "Pelajar/Mahasiswa": 44,
        "Pelaut": 45,
        "Pembantu Rumah Tangga": 46,
        "Penata Busana": 47,
        "Penata Rambut": 48,
        "Penata Rias": 49,
        "Pendeta": 50,
        "Peneliti": 51,
        "Pengacara": 52,
        "Pensiunan": 53,
        "Penterjemah": 54,
        "Penyiar Radio": 55,
        "Penyiar Televisi": 56,
        "Perancang Busana": 57,
        "Perangkat Desa": 58,
        "Perawat": 59,
        "Perdagangan": 60,
        "Petani/Pekebun/Peternak": 61,
        "Pialang": 62,
        "Pilot": 63,
        "Promotor Acara": 64,
        "Psikiater/Psikolog": 65,
        "Seniman": 66,
        "Sopir": 67,
        "Tabib": 68,
        "Tentara Nasional Indonesia": 69,
        "Transportasi": 70,
        "Tukang Batu": 71,
        "Tukang Cukur": 72,
        "Tukang Gigi": 73,
        "Tukang Jahit": 74,
        "Tukang Kayu": 75,
        "Tukang Las/Pandai Besi": 76,
        "Tukang Listrik": 77,
        "Tukang Sol Sepatu": 78,
        "Ustadz/Mubaligh": 79,
        "Wakil Gubernur": 80,
        "Wakil Presiden": 81,
        "Walikota": 82,
        "Wartawan": 83,
        "Wiraswasta": 84  
    }

    if category == "education":
        return education_list[field]
    elif category == "occupation":
        return occupation_list[field]

def get_field_list(collection):
    """
    Get list of all non-spacetime fields in a standard 
    collection document
    """
    # list all space/time/id fields in document
    spacetimeid_list = ['Kecamatan', 'Kabupaten', 'Kelurahan', 
                        'Tahun', "_id"]
    # list all education level fields
    return [field for field in list(collection.find_one().keys()) 
            if field not in spacetimeid_list]