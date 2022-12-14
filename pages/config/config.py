YEAR_RANGE = [i for i in range(1989, 2020)]

TRADE_STATS = [
  'Agricultural Raw Materials',
  'Animal'
  'Capital goods'
  'Chemical'
  'Consumer goods'
  'Food Products'
  'Food'
  'Footwear'
  'Fuels'
  'Intermediate goods'
  'Mach and Elec'
  'Machinery and Transport Equipment'
  'Manufactures'
  'Metals'
  'Minerals'
  'Miscellaneous'
  'Ores and Metals'
  'Plastic or Rubber'
  'Raw materials'
  'Stone and Glass'
  'Textiles and Clothing'
  'Textiles'
  'Transportation'
  'Vegetable'
  'Wood'
]

REGIONS = [
  "East Asia & Pacific", "Europe & Central Asia", "Middle East & North Africa",
  "North America", "South Asia", "Sub-Saharan Africa",
  "Latin America & Caribbean"
]

COUNTRY_REG = {
  'Afghanistan': REGIONS[4],
  'Albania': REGIONS[1],
  'Algeria': REGIONS[2],
  'American Samoa': REGIONS[0],
  'Angola': REGIONS[5],
  'Antigua and Barbuda': REGIONS[6],
  'Argentina': REGIONS[6],
  'Armenia': REGIONS[1],
  'Aruba': REGIONS[6],
  'Australia': REGIONS[0],
  'Austria': REGIONS[1],
  'Azerbaijan': REGIONS[1],
  'Bahamas': REGIONS[6],
  'Bahrain': REGIONS[2],
  'Bangladesh': REGIONS[4],
  'Barbados': REGIONS[6],
  'Belgium': REGIONS[1],
  'Belize': REGIONS[6],
  'Bermuda': REGIONS[3],
  'Bhutan': REGIONS[4],
  'Bolivia': REGIONS[6],
  'Bosnia and Herzegovina': REGIONS[1],
  'Brazil': REGIONS[6],
  'Brunei': REGIONS[0],
  'Bulgaria': REGIONS[1],
  'Burundi': REGIONS[5],
  'Cambodia': REGIONS[0],
  'Cameroon': REGIONS[5],
  'Canada': REGIONS[3],
  'Cape Verde': REGIONS[5],
  'Cayman Islands': REGIONS[6],
  'Central African Republic': REGIONS[5],
  'Chile': REGIONS[6],
  'China': REGIONS[0],
  'Colombia': REGIONS[6],
  'Comoros': REGIONS[5],
  'Congo [DRC]': REGIONS[5],
  'Congo [Republic]': REGIONS[5],
  'Costa Rica': REGIONS[6],
  "Cote d'Ivoire": REGIONS[5],
  'Croatia': REGIONS[1],
  'Cuba': REGIONS[6],
  'Curaçao': REGIONS[6],
  'Cyprus': REGIONS[1],
  'Czech Republic': REGIONS[1],
  'Denmark': REGIONS[1],
  'Djibouti': REGIONS[2],
  'Dominica': REGIONS[6],
  'Dominican Republic': REGIONS[6],
  'East Timor': REGIONS[0],
  'Ecuador': REGIONS[6],
  'Egypt': REGIONS[2],
  'El Salvador': REGIONS[6],
  'Equatorial Guinea': REGIONS[5],
  'Eritrea': REGIONS[5],
  'Estonia': REGIONS[1],
  'Eswatini': REGIONS[5],
  'Ethiopia': REGIONS[5],
  'Faeroe Islands': REGIONS[1],
  'Fiji': REGIONS[0],
  'Finland': REGIONS[1],
  'Sudan': REGIONS[5],
  'France': REGIONS[1],
  'French Polynesia': REGIONS[0],
  'Gambia': REGIONS[5],
  'Georgia': REGIONS[1],
  'Germany': REGIONS[1],
  'Ghana': REGIONS[5],
  'Greece': REGIONS[1],
  'Greenland': REGIONS[1],
  'Grenada': REGIONS[6],
  'Guam': REGIONS[0],
  'Guatemala': REGIONS[6],
  'Guinea': REGIONS[5],
  'Guyana': REGIONS[6],
  'Haiti': REGIONS[6],
  'Honduras': REGIONS[6],
  'Hong Kong': REGIONS[0],
  'Hungary': REGIONS[1],
  'Iceland': REGIONS[1],
  'India': REGIONS[4],
  'Indonesia': REGIONS[0],
  'Iran': REGIONS[2],
  'Iraq': REGIONS[2],
  'Ireland': REGIONS[1],
  'Israel': REGIONS[2],
  'Italy': REGIONS[1],
  'Jamaica': REGIONS[6],
  'Japan': REGIONS[0],
  'Jordan': REGIONS[2],
  'Kazakhstan': REGIONS[1],
  'Kenya': REGIONS[5],
  'Kiribati': REGIONS[0],
  'North Korea': REGIONS[0],
  'South Korea': REGIONS[0],
  'Kuwait': REGIONS[2],
  'Kyrgyzstan': REGIONS[1],
  'Laos': REGIONS[0],
  'Latvia': REGIONS[1],
  'Lebanon': REGIONS[2],
  'Liberia': REGIONS[5],
  'Libya': REGIONS[2],
  'Lithuania': REGIONS[1],
  'Luxembourg': REGIONS[1],
  'Macao': REGIONS[0],
  'Madagascar': REGIONS[5],
  'Malawi': REGIONS[5],
  'Malaysia': REGIONS[0],
  'Maldives': REGIONS[4],
  'Mali': REGIONS[5],
  'Malta': REGIONS[2],
  'Marshall Islands': REGIONS[0],
  'Mexico': REGIONS[6],
  'Micronesia': REGIONS[0],
  'Moldova': REGIONS[1],
  'Monaco': REGIONS[1],
  'Mongolia': REGIONS[0],
  'Morocco': REGIONS[2],
  'Mozambique': REGIONS[5],
  'Myanmar [Burma]': REGIONS[0],
  'Nepal': REGIONS[4],
  'Netherlands': REGIONS[1],
  'New Caledonia': REGIONS[0],
  'New Zealand': REGIONS[0],
  'Niger': REGIONS[5],
  'Nigeria': REGIONS[5],
  'North Macedonia': REGIONS[1],
  'Northern Mariana Islands': REGIONS[0],
  'Norway': REGIONS[1],
  'Oman': REGIONS[2],
  'Pakistan': REGIONS[4],
  'Palau': REGIONS[0],
  'Panama': REGIONS[6],
  'Papua New Guinea': REGIONS[0],
  'Paraguay': REGIONS[6],
  'Peru': REGIONS[6],
  'Philippines': REGIONS[0],
  'Poland': REGIONS[1],
  'Portugal': REGIONS[1],
  'Qatar': REGIONS[2],
  'Romania': REGIONS[1],
  'Russia': REGIONS[1],
  'Rwanda': REGIONS[5],
  'Samoa': REGIONS[0],
  'San Marino': REGIONS[1],
  'Saudi Arabia': REGIONS[2],
  'Senegal': REGIONS[5],
  'Seychelles': REGIONS[5],
  'Sierra Leone': REGIONS[5],
  'Slovakia': REGIONS[1],
  'Slovenia': REGIONS[1],
  'Solomon Islands': REGIONS[0],
  'Somalia': REGIONS[5],
  'South Africa': REGIONS[5],
  'South Sudan': REGIONS[5],
  'Spain': REGIONS[1],
  'Sri Lanka': REGIONS[4],
  'Saint Kitts and Nevis': REGIONS[6],
  'Saint Lucia': REGIONS[6],
  'Saint Vincent and the Grenadines': REGIONS[6],
  'Suriname': REGIONS[6],
  'Sweden': REGIONS[1],
  'Switzerland': REGIONS[1],
  'Syria': REGIONS[2],
  'Tajikistan': REGIONS[1],
  'Tanzania': REGIONS[5],
  'Thailand': REGIONS[0],
  'Togo': REGIONS[5],
  'Tonga': REGIONS[0],
  'Trinidad and Tobago': REGIONS[6],
  'Tunisia': REGIONS[2],
  'Turkey': REGIONS[1],
  'Turkmenistan': REGIONS[1],
  'Turks and Caicos Islands': REGIONS[6],
  'Tuvalu': REGIONS[0],
  'Uganda': REGIONS[5],
  'Ukraine': REGIONS[1],
  'United Arab Emirates': REGIONS[2],
  'United Kingdom': REGIONS[1],
  'United States': REGIONS[3],
  'Uruguay': REGIONS[6],
  'Uzbekistan': REGIONS[1],
  'Vanuatu': REGIONS[0],
  'Venezuela': REGIONS[6],
  'Vietnam': REGIONS[0],
  'Yemen': REGIONS[2],
  'Yemen Democratic': REGIONS[2],
  'Zambia': REGIONS[5],
  'Zimbabwe': REGIONS[5],
}
