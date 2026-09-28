import { useMemo, useState } from 'react'
import './App.css'
import { getVoterMatch } from './voterValidation.js'

const districtCatalog = {
  'Andhra Pradesh': ['Anantapur', 'Chittoor', 'East Godavari', 'Guntur', 'Krishna', 'Kurnool', 'Nellore', 'Prakasam', 'Srikakulam', 'Visakhapatnam', 'Vizianagaram', 'West Godavari'],
  'Arunachal Pradesh': ['Anjaw', 'Changlang', 'Dibang Valley', 'East Kameng', 'East Siang', 'Kamle', 'Kra Daadi', 'Kurung Kumey', 'Lohit', 'Longding', 'Lower Dibang Valley', 'Lower Siang', 'Lower Subansiri', 'Namsai', 'Papum Pare', 'Siang', 'Tawang', 'Tirap', 'Upper Dibang Valley', 'Upper Siang', 'Upper Subansiri', 'West Kameng', 'West Siang'],
  'Assam': ['Baksa', 'Barpeta', 'Biswanath', 'Bongaigaon', 'Cachar', 'Charaideo', 'Chirang', 'Darrang', 'Dhemaji', 'Dhubri', 'Dibrugarh', 'Dima Hasao', 'Goalpara', 'Golaghat', 'Hailakandi', 'Hojai', 'Jorhat', 'Kamrup Metropolitan', 'Kamrup Rural', 'Karbi Anglong', 'Karimganj', 'Kokrajhar', 'Lakhimpur', 'Majuli', 'Morigaon', 'Nagaon', 'Nalbari', 'Sivasagar', 'Sonitpur', 'South Salmara-Mankachar', 'Tinsukia', 'Udalguri', 'West Karbi Anglong'],
  'Bihar': ['Araria', 'Arwal', 'Aurangabad', 'Banka', 'Begusarai', 'Bhagalpur', 'Bhojpur', 'Buxar', 'Darbhanga', 'East Champaran', 'Gaya', 'Gopalganj', 'Jamui', 'Jehanabad', 'Kaimur', 'Katihar', 'Khagaria', 'Kishanganj', 'Lakhisarai', 'Madhepura', 'Madhubani', 'Munger', 'Muzaffarpur', 'Nawada', 'Patna', 'Purnia', 'Rohtas', 'Saharsa', 'Samastipur', 'Saran', 'Sheikhpura', 'Sheohar', 'Sitamarhi', 'Siwan', 'Supaul', 'Vaishali', 'West Champaran'],
  'Chhattisgarh': ['Balod', 'Baloda Bazar', 'Balrampur', 'Bastar', 'Bemetara', 'Bijapur', 'Bilaspur', 'Dantewada', 'Dhamtari', 'Durg', 'Gariaband', 'Gaurela-Pendra-Marwahi', 'Janjgir-Champa', 'Jashpur', 'Kabirdham', 'Kanker', 'Kondagaon', 'Korba', 'Koriya', 'Mahasamund', 'Mungeli', 'Narayanpur', 'Raigarh', 'Raipur', 'Rajnandgaon', 'Sarangarh-Bilaigarh', 'Sukma', 'Surajpur', 'Surguja'],
  'Goa': ['North Goa', 'South Goa'],
  'Gujarat': ['Ahmedabad', 'Amreli', 'Anand', 'Aravalli', 'Banaskantha', 'Bharuch', 'Bhavnagar', 'Botad', 'Chhota Udaipur', 'Dahod', 'Dang', 'Devbhoomi Dwarka', 'Gandhinagar', 'Gir Somnath', 'Jamnagar', 'Junagadh', 'Kheda', 'Kutch', 'Mahisagar', 'Mehsana', 'Morbi', 'Narmada', 'Navsari', 'Panchmahal', 'Patan', 'Porbandar', 'Rajkot', 'Sabarkantha', 'Surat', 'Surendranagar', 'Tapi', 'Vadodara', 'Valsad'],
  'Haryana': ['Ambala', 'Bhiwani', 'Charkhi Dadri', 'Faridabad', 'Fatehabad', 'Gurugram', 'Hisar', 'Jhajjar', 'Jind', 'Kaithal', 'Karnal', 'Kurukshetra', 'Mahendragarh', 'Nuh', 'Palwal', 'Panchkula', 'Panipat', 'Rewari', 'Rohtak', 'Sirsa', 'Sonipat', 'Yamunanagar'],
  'Himachal Pradesh': ['Bilaspur', 'Chamba', 'Hamirpur', 'Kangra', 'Kinnaur', 'Kullu', 'Lahaul and Spiti', 'Mandi', 'Shimla', 'Sirmaur', 'Solan', 'Una'],
  'Jharkhand': ['Bokaro', 'Chatra', 'Deoghar', 'Dhanbad', 'Dumka', 'East Singhbhum', 'Garhwa', 'Giridih', 'Godda', 'Gumla', 'Hazaribagh', 'Jamtara', 'Khunti', 'Koderma', 'Latehar', 'Lohardaga', 'Pakur', 'Palamu', 'Ramgarh', 'Ranchi', 'Sahibganj', 'Seraikela Kharsawan', 'Simdega', 'West Singhbhum'],
  'Karnataka': ['Bagalkot', 'Bangalore Rural', 'Bengaluru Urban', 'Belagavi', 'Bellary', 'Bidar', 'Chamarajanagar', 'Chikkaballapur', 'Chikkamagaluru', 'Chitradurga', 'Dakshina Kannada', 'Davanagere', 'Dharwad', 'Gadag', 'Hassan', 'Haveri', 'Kalaburagi', ' Kodagu', 'Kolar', 'Koppal', 'Mandya', 'Mysuru', 'Raichur', 'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada', 'Vijayanagara', 'Vijayapura', 'Yadgir'],
  'Kerala': ['Alappuzha', 'Ernakulam', 'Idukki', 'Kannur', 'Kasaragod', 'Kollam', 'Kottayam', 'Kozhikode', 'Malappuram', 'Palakkad', 'Pathanamthitta', 'Thiruvananthapuram', 'Thrissur', 'Wayanad'],
  'Madhya Pradesh': ['Agar Malwa', 'Alirajpur', 'Anuppur', 'Ashoknagar', 'Balaghat', 'Barwani', 'Betul', 'Bhind', 'Bhopal', 'Burhanpur', 'Chhatarpur', 'Chhindwara', 'Damoh', 'Datia', 'Dewas', 'Dhar', 'Dindori', 'Guna', 'Gwalior', 'Harda', 'Hoshangabad', 'Indore', 'Jabalpur', 'Jhabua', 'Katni', 'Khandwa', 'Khargone', 'Mandla', 'Mandsaur', 'Morena', 'Narsinghpur', 'Neemuch', 'Panna', 'Raisen', 'Rajgarh', 'Ratlam', 'Rewa', 'Sagar', 'Satna', 'Sehore', 'Seoni', 'Shahdol', 'Shajapur', 'Sheopur', 'Shivpuri', 'Sidhi', 'Singrauli', 'Tikamgarh', 'Ujjain', 'Umaria', 'Vidisha'],
  'Maharashtra': ['Ahmednagar', 'Akola', 'Amravati', 'Aurangabad', 'Beed', 'Bhandara', 'Buldhana', 'Chandrapur', 'Dhule', 'Gadchiroli', 'Gondia', 'Hingoli', 'Jalgaon', 'Jalna', 'Kolhapur', 'Latur', 'Mumbai City', 'Mumbai Suburban', 'Nagpur', 'Nanded', 'Nandurbar', 'Nashik', 'Osmanabad', 'Palghar', 'Parbhani', 'Pune', 'Raigad', 'Ratnagiri', 'Sangli', 'Satara', 'Sindhudurg', 'Solapur', 'Thane', 'Wardha', 'Washim', 'Yavatmal'],
  'Manipur': ['Bishnupur', 'Chandel', 'Churachandpur', 'Imphal East', 'Imphal West', 'Jiribam', 'Kakching', 'Kamjong', 'Kangpokpi', 'Noney', 'Pherzawl', 'Senapati', 'Tamenglong', 'Tengnoupal', 'Thoubal', 'Ukhrul'],
  'Meghalaya': ['East Garo Hills', 'East Jaintia Hills', 'East Khasi Hills', 'North Garo Hills', 'Ri Bhoi', 'South Garo Hills', 'South West Garo Hills', 'South West Khasi Hills', 'West Garo Hills', 'West Jaintia Hills', 'West Khasi Hills'],
  'Mizoram': ['Aizawl', 'Champhai', 'Hnahthial', 'Kolasib', 'Lawngtlai', 'Lunglei', 'Mamit', 'Saiha', 'Saitual', 'Serchhip'],
  'Nagaland': ['Chumoukedima', 'Dimapur', 'Kiphire', 'Kohima', 'Longleng', 'Mokokchung', 'Mon', 'Niuland', 'Peren', 'Phek', 'Phompena', 'Shamator', 'Tseminyü', 'Tuensang', 'Wokha', 'Zunheboto'],
  'Odisha': ['Angul', 'Balangir', 'Balasore', 'Bargarh', 'Bhadrak', 'Boudh', 'Cuttack', 'Deogarh', 'Dhenkanal', 'Gajapati', 'Ganjam', 'Jagatsinghpur', 'Jajpur', 'Jharsuguda', 'Kalahandi', 'Kandhamal', 'Kendrapara', 'Kendujhar', 'Khordha', 'Koraput', 'Malkangiri', 'Mayurbhanj', 'Nabarangpur', 'Nayagarh', 'Nuapada', 'Puri', 'Rayagada', 'Sambalpur', 'Subarnapur', 'Sundergarh'],
  'Punjab': ['Amritsar', 'Barnala', 'Bathinda', 'Faridkot', 'Fatehgarh Sahib', 'Fazilka', 'Ferozepur', 'Gurdaspur', 'Hoshiarpur', 'Jalandhar', 'Kapurthala', 'Ludhiana', 'Mansa', 'Moga', 'Mohali', 'Muktsar', 'Nawanshahr', 'Pathankot', 'Patiala', 'Rupnagar', 'Sangrur', 'Shaheed Bhagat Singh Nagar', 'Tarn Taran'],
  'Rajasthan': ['Ajmer', 'Alwar', 'Anupgarh', 'Balotra', 'Banswara', 'Baran', 'Barmer', 'Beawar', 'Bikaner', 'Bundi', 'Chittorgarh', 'Churu', 'Dausa', 'Deeg', 'Dholpur', 'Didwana-Kuchaman', 'Dungarpur', 'Ganganagar', 'Gangapur City', 'Hanumangarh', 'Jaipur', 'Jaisalmer', 'Jalore', 'Jhalawar', 'Jhunjhunu', 'Jodhpur', 'Karauli', 'Kehsi', 'Khairthal-Tijara', 'Kota', 'Nagaur', 'Pali', 'Phalodi', 'Rajsamand', 'Salumber', 'Sanchore', 'Sawai Madhopur', 'Shahpura', 'Sikar', 'Sirohi', 'Sojat', 'Tonk', 'Udaipur'],
  'Sikkim': ['East Sikkim', 'North Sikkim', 'South Sikkim', 'West Sikkim'],
  'Tamil Nadu': ['Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul', 'Erode', 'Kallakurichi', 'Kancheepuram', 'Karur', 'Krishnagiri', 'Madurai', 'Mayiladuthurai', 'Nagapattinam', 'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai', 'Ramanathapuram', 'Ranipet', 'Salem', 'Sivaganga', 'Tenkasi', 'Thanjavur', 'Theni', 'Thoothukudi', 'Tiruchirappalli', 'Tirunelveli', 'Tirupathur', 'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Vellore', 'Viluppuram', 'Virudhunagar'],
  'Telangana': ['Adilabad', 'Bhadradri Kothagudem', 'Hanumakonda', 'Hyderabad', 'Jagitial', 'Jangoan', 'Jayashankar Bhupalpally', 'Jogulamba Gadwal', 'Kamareddy', 'Karimnagar', 'Khammam', 'Komaram Bheem Asifabad', 'Mahabubabad', 'Mahabubnagar', 'Mancherial', 'Medak', 'Medchal-Malkajgiri', 'Mulugu', 'Nagarkurnool', 'Nalgonda', 'Narayanpet', 'Nirmal', 'Nizamabad', 'Peddapalli', 'Rajanna Sircilla', 'Ranga Reddy', 'Sangareddy', 'Siddipet', 'Suryapet', 'Vikarabad', 'Wanaparthy', 'Warangal', 'Yadadri Bhuvanagiri'],
  'Tripura': ['Dhalai', 'Gomati', 'Khowai', 'North Tripura', 'Sepahijala', 'South Tripura', 'Unakoti', 'West Tripura'],
  'Uttar Pradesh': ['Agra', 'Aligarh', 'Ambedkar Nagar', 'Amethi', 'Amroha', 'Auraiya', 'Ayodhya', 'Azamgarh', 'Badaun', 'Baghpat', 'Bahraich', 'Ballia', 'Balrampur', 'Banda', 'Barabanki', 'Bareilly', 'Basti', 'Behat', 'Bhadohi', 'Bijnor', 'Budaun', 'Bulandshahr', 'Chandauli', 'Chitrakoot', 'Deoria', 'Etah', 'Etawah', 'Faizabad', 'Farrukhabad', 'Fatehpur', 'Firozabad', 'Gautam Buddha Nagar', 'Ghaziabad', 'Ghazipur', 'Gonda', 'Gorakhpur', 'Hamirpur', 'Hapur', 'Hardoi', 'Hathras', 'Jalaun', 'Jaunpur', 'Jhansi', 'Kannauj', 'Kanpur Dehat', 'Kanpur Nagar', 'Kasganj', 'Kaushambi', 'Kushinagar', 'Lakhimpur Kheri', 'Lalitpur', 'Lucknow', 'Maharajganj', 'Mahoba', 'Mainpuri', 'Mathura', 'Mau', 'Meerut', 'Mirzapur', 'Moradabad', 'Muzaffarnagar', 'Pilibhit', 'Pratapgarh', 'Rae Bareli', 'Rampur', 'Saharanpur', 'Sambhal', 'Sant Kabir Nagar', 'Shahjahanpur', 'Shamli', 'Shravasti', 'Siddharthnagar', 'Sitapur', 'Sonbhadra', 'Sultanpur', 'Unnao', 'Varanasi'],
  'Uttarakhand': ['Almora', 'Bageshwar', 'Chamoli', 'Champawat', 'Dehradun', 'Haridwar', 'Nainital', 'Pauri Garhwal', 'Pithoragarh', 'Rudraprayag', 'Tehri Garhwal', 'Udham Singh Nagar', 'Uttarkashi'],
  'West Bengal': ['Alipurduar', 'Bankura', 'Birbhum', 'Cooch Behar', 'Dakshin Dinajpur', 'Darjeeling', 'Hooghly', 'Howrah', 'Jalpaiguri', 'Jhargram', 'Kalimpong', 'Kolkata', 'Malda', 'Murshidabad', 'Nadia', 'North 24 Parganas', 'Paschim Bardhaman', 'Paschim Medinipur', 'Purba Bardhaman', 'Purba Medinipur', 'Purulia', 'South 24 Parganas', 'Uttar Dinajpur'],
  'Andaman and Nicobar Islands': ['Nicobar', 'North and Middle Andaman', 'South Andaman'],
  'Chandigarh': ['Chandigarh'],
  'Dadra and Nagar Haveli and Daman and Diu': ['Daman', 'Diu', 'Dadra and Nagar Haveli'],
  'Delhi': ['Central Delhi', 'East Delhi', 'New Delhi', 'North Delhi', 'North East Delhi', 'North West Delhi', 'Shahdara', 'South Delhi', 'South East Delhi', 'South West Delhi', 'West Delhi'],
  'Jammu and Kashmir': ['Anantnag', 'Bandipora', 'Baramulla', 'Budgam', 'Doda', 'Ganderbal', 'Jammu', 'Kathua', 'Kishtwar', 'Kulgam', 'Kupwara', 'Pulwama', 'Rajouri', 'Ramban', 'Reasi', 'Samba', 'Shopian', 'Srinagar', 'Udhampur', 'Bandipora'],
  'Ladakh': ['Kargil', 'Leh'],
  'Lakshadweep': ['Agatti', 'Amini', 'Andrott', 'Bitra', 'Chetlat', 'Kadmat', 'Kavaratti', 'Kilthan', 'Minicoy'],
  'Puducherry': ['Karaikal', 'Mahe', 'Puducherry', 'Yanam']
}

const stateOptions = Object.keys(districtCatalog)
const palette = ['#f7b731', '#56ccf2', '#2ecc71', '#b084f5', '#ff6b6b', '#ffcd29']
const defaultParties = ['BJP', 'INC', 'AAP', 'CPI(M)', 'CPI', 'SP', 'TMC', 'DMK', 'NCP', 'BSP', 'TDP', 'AIADMK', 'JD(U)', 'RJD', 'SS', 'AITC', 'NPP', 'MNM', 'VCK', 'PMK']

const stateParties = {
  'Andhra Pradesh': ['TDP', 'YSRCP', 'Janasena', 'BJP', 'INC', 'CPI(M)', 'CPI', 'BSP'],
  'Assam': ['BJP', 'INC', 'AGP', 'AAP', 'AIUDF', 'CPI(M)', 'BSP', 'CPI'],
  'Bihar': ['JD(U)', 'RJD', 'BJP', 'INC', 'HAM(S)', 'CPI(ML)', 'BSP', 'CPI(M)', 'AIPF'],
  'Chhattisgarh': ['BJP', 'INC', 'BSP', 'CPI(M)', 'CPI', 'GGP', 'JCC(J)'],
  'Goa': ['BJP', 'INC', 'AAP', 'MGP', 'TMC', 'BSP', 'CPI'],
  'Gujarat': ['BJP', 'INC', 'AAP', 'BSP', 'CPI(M)', 'CPI', 'GPP'],
  'Haryana': ['BJP', 'INC', 'AAP', 'INLD', 'BSP', 'CPI(M)', 'CPI'],
  'Himachal Pradesh': ['BJP', 'INC', 'AAP', 'BSP', 'CPI(M)'],
  'Jharkhand': ['JMM', 'BJP', 'INC', 'AJSU', 'RJD', 'CPI(ML)', 'BSP', 'CPI(M)'],
  'Karnataka': ['INC', 'BJP', 'JDS', 'AAP', 'CPI(M)', 'CPI', 'BSP', 'SDP'],
  'Kerala': ['INC', 'CPI(M)', 'BJP', 'CPI', 'IUML', 'KC(M)', 'RSP', 'BSP', 'NCP'],
  'Madhya Pradesh': ['BJP', 'INC', 'BSP', 'AAP', 'CPI(M)', 'CPI', 'SP'],
  'Maharashtra': ['BJP', 'INC', 'SS', 'NCP', 'SHS', 'SP', 'MNS', 'CPI(M)', 'CPI', 'BSP', 'AIMIM'],
  'Manipur': ['BJP', 'INC', 'NPP', 'AAP', 'CPI', 'BSP', 'NCP'],
  'Meghalaya': ['NPP', 'INC', 'UDP', 'BJP', 'VPP', 'BSP', 'CPI(M)'],
  'Mizoram': ['MNF', 'ZPM', 'INC', 'BJP', 'BSP', 'CPI(M)'],
  'Nagaland': ['NDPP', 'BJP', 'INC', 'NPF', 'BSP', 'CPI(M)'],
  'Odisha': ['BJD', 'BJP', 'INC', 'CPI(M)', 'CPI', 'BSP', 'AAP'],
  'Punjab': ['AAP', 'INC', 'BJP', 'SAD', 'BSP', 'CPI(M)', 'CPI', 'SAD (Amritsar)'],
  'Rajasthan': ['BJP', 'INC', 'BSP', 'AAP', 'CPI(M)', 'CPI', 'RLP'],
  'Sikkim': ['SKM', 'SDF', 'BJP', 'INC', 'BSP'],
  'Tamil Nadu': ['DMK', 'AIADMK', 'BJP', 'INC', 'VCK', 'MNM', 'PMK', 'TVK', 'NTK', 'CPI(M)', 'CPI', 'AMMK', 'BSP'],
  'Telangana': ['BRS', 'INC', 'BJP', 'AIMIM', 'CPI(M)', 'CPI', 'BSP'],
  'Tripura': ['BJP', 'Tipra Motha', 'INC', 'CPI(M)', 'CPI', 'BSP'],
  'Uttar Pradesh': ['BJP', 'SP', 'INC', 'BSP', 'AAP', 'RLD', 'CPI(M)', 'CPI', 'SBSP', 'NISHAD'],
  'Uttarakhand': ['BJP', 'INC', 'AAP', 'BSP', 'CPI(M)', 'CPI', 'UKD'],
  'West Bengal': ['TMC', 'BJP', 'INC', 'CPM', 'CPI', 'BSP', 'AAP', 'SUCI'],
  'Andaman and Nicobar Islands': ['BJP', 'INC', 'AAP', 'BSP', 'CPI(M)'],
  'Chandigarh': ['BJP', 'INC', 'AAP', 'BSP', 'CPI(M)'],
  'Dadra and Nagar Haveli and Daman and Diu': ['BJP', 'INC', 'AAP', 'BSP', 'CPI(M)'],
  'Delhi': ['AAP', 'BJP', 'INC', 'BSP', 'CPI(M)', 'CPI'],
  'Jammu and Kashmir': ['NC', 'BJP', 'INC', 'PDP', 'AAP', 'BSP', 'CPI(M)'],
  'Ladakh': ['BJP', 'INC', 'AAP', 'BSP', 'CPI(M)'],
  'Lakshadweep': ['INC', 'BJP', 'CPI(M)', 'BSP', 'AAP'],
  'Puducherry': ['INC', 'DMK', 'BJP', 'AIMIM', 'BSP', 'CPI(M)'],
}

const nationalPmParties = ['BJP', 'INC', 'AAP', 'CPI(M)', 'CPI', 'SP', 'TMC', 'NCP', 'BSP', 'DMK', 'TDP', 'AIMIM', 'SS', 'RJD', 'JD(U)', 'BJD', 'SHS', 'MNS']

const validVoterRecords = [
  { username: '123456789012', aadhaar: '123456789012', voterId: 'VOT-00149' },
  { username: '234567890123', aadhaar: '234567890123', voterId: 'VOT-00462' },
  { username: '345678901234', aadhaar: '345678901234', voterId: 'VOT-00813' },
  { username: '456789012345', aadhaar: '456789012345', voterId: 'VOT-01274' },
  { username: 'VOT-00149', aadhaar: '123456789012', voterId: 'VOT-00149' },
  { username: 'VOT-00462', aadhaar: '234567890123', voterId: 'VOT-00462' },
  { username: 'VOT-00813', aadhaar: '345678901234', voterId: 'VOT-00813' },
  { username: 'VOT-01274', aadhaar: '456789012345', voterId: 'VOT-01274' },
]

const tamilNaduCMDistrictLeaders = {
  'Ariyalur': 'M. K. Stalin',
  'Chengalpattu': 'C. Joseph Vijay',
  'Chennai': 'C. Joseph Vijay',
  'Coimbatore': 'C. Joseph Vijay',
  'Cuddalore': 'M. K. Stalin',
  'Dharmapuri': 'C. Joseph Vijay',
  'Dindigul': 'C. Joseph Vijay',
  'Erode': 'C. Joseph Vijay',
  'Kallakurichi': 'M. K. Stalin',
  'Kancheepuram': 'C. Joseph Vijay',
  'Karur': 'C. Joseph Vijay',
  'Krishnagiri': 'C. Joseph Vijay',
  'Madurai': 'C. Joseph Vijay',
  'Mayiladuthurai': 'M. K. Stalin',
  'Nagapattinam': 'M. K. Stalin',
  'Namakkal': 'C. Joseph Vijay',
  'Nilgiris': 'C. Joseph Vijay',
  'Perambalur': 'M. K. Stalin',
  'Pudukkottai': 'M. K. Stalin',
  'Ramanathapuram': 'M. K. Stalin',
  'Ranipet': 'C. Joseph Vijay',
  'Salem': 'C. Joseph Vijay',
  'Sivaganga': 'M. K. Stalin',
  'Tenkasi': 'M. K. Stalin',
  'Thanjavur': 'M. K. Stalin',
  'Theni': 'C. Joseph Vijay',
  'Thoothukudi': 'M. K. Stalin',
  'Tiruchirappalli': 'M. K. Stalin',
  'Tirunelveli': 'M. K. Stalin',
  'Tirupathur': 'C. Joseph Vijay',
  'Tiruppur': 'C. Joseph Vijay',
  'Tiruvallur': 'C. Joseph Vijay',
  'Tiruvannamalai': 'M. K. Stalin',
  'Tiruvarur': 'M. K. Stalin',
  'Vellore': 'C. Joseph Vijay',
  'Viluppuram': 'M. K. Stalin',
  'Virudhunagar': 'M. K. Stalin',
}

const tamilNaduDistrictPartyMap = {
  'Ariyalur': 'DMK',
  'Chengalpattu': 'TVK',
  'Chennai': 'TVK',
  'Coimbatore': 'TVK',
  'Cuddalore': 'DMK',
  'Dharmapuri': 'TVK',
  'Dindigul': 'TVK',
  'Erode': 'TVK',
  'Kallakurichi': 'DMK',
  'Kancheepuram': 'TVK',
  'Karur': 'TVK',
  'Krishnagiri': 'TVK',
  'Madurai': 'TVK',
  'Mayiladuthurai': 'DMK',
  'Nagapattinam': 'DMK',
  'Namakkal': 'TVK',
  'Nilgiris': 'TVK',
  'Perambalur': 'DMK',
  'Pudukkottai': 'DMK',
  'Ramanathapuram': 'DMK',
  'Ranipet': 'TVK',
  'Salem': 'TVK',
  'Sivaganga': 'DMK',
  'Tenkasi': 'DMK',
  'Thanjavur': 'DMK',
  'Theni': 'TVK',
  'Thoothukudi': 'DMK',
  'Tiruchirappalli': 'DMK',
  'Tirunelveli': 'DMK',
  'Tirupathur': 'TVK',
  'Tiruppur': 'TVK',
  'Tiruvallur': 'TVK',
  'Tiruvannamalai': 'DMK',
  'Tiruvarur': 'DMK',
  'Vellore': 'TVK',
  'Viluppuram': 'DMK',
  'Virudhunagar': 'DMK',
}

const tamilNaduThoguthiCatalog = Object.fromEntries(
  districtCatalog['Tamil Nadu'].map((districtName) => [districtName, [
    `${districtName} Assembly Constituency`,
    `${districtName} North`,
    `${districtName} South`,
  ]]),
)

const electionHighlights = [
  { icon: '◎', title: 'Identity verification', text: 'Aadhaar-linked checks validate each voter identity before a ballot is activated.' },
  { icon: '▣', title: 'Distributed ledger', text: 'Vote blocks are synchronized across validators for transparent and tamper-resistant recording.' },
  { icon: '⬡', title: 'Zero-knowledge audit', text: 'Election observers can verify integrity without exposing personal vote details.' },
  { icon: '⌁', title: 'Disaster recovery', text: 'Cross-state validator redundancy maintains continuity during outages and cyber incidents.' },
  { icon: '◈', title: 'Result validation', text: 'Vote totals are cross-checked at district, state, and national levels before publication.' },
  { icon: '✦', title: 'Accessible polling', text: 'Support for multilingual voting interfaces and accessibility-aware district workflows.' },
]

const featureChecklist = [
  { title: 'Voter registration and authentication', text: 'Citizens are onboarded with a secure identity profile and verified against the official voter registry before polls open.' },
  { title: 'One-person-one-vote mechanism', text: 'Each eligible voter receives a single ballot token and the system blocks duplicate participation across the election window.' },
  { title: 'Blockchain-based vote recording', text: 'Every ballot is hashed, chained, and stored as a tamper-evident block on the election ledger before final tallying.' },
  { title: 'Smart contract for election management', text: 'Election rules are enforced through policy checks for validation, voter eligibility, and safe publication of results.' },
  { title: 'Real-time vote counting', text: 'Live tallies update as votes are validated, allowing districts and states to monitor election progress in real time.' },
  { title: 'Tamper-evident election records', text: 'Ledger integrity checks and block hashes allow the public to confirm that historical records have not been altered.' },
  { title: 'Admin dashboard', text: 'Election administrators monitor validators, vote history, result publication, and control-room operations through a secure dashboard.' },
]

const topTransactionRecords = [
  { id: 'TX-40821', block: 9842119, sender: 'Voter 4A8D', receiver: 'State Ledger', amount: '0.028 ETH', status: 'Confirmed' },
  { id: 'TX-40822', block: 9842120, sender: 'Election Node 12', receiver: 'Audit Vault', amount: '0.036 ETH', status: 'Confirmed' },
  { id: 'TX-40823', block: 9842121, sender: 'Voter 9C2F', receiver: 'State Ledger', amount: '0.020 ETH', status: 'Pending' },
  { id: 'TX-40824', block: 9842123, sender: 'Validator 7', receiver: 'Security Pool', amount: '0.041 ETH', status: 'Confirmed' },
  { id: 'TX-40825', block: 9842127, sender: 'Voter 2FA1', receiver: 'State Ledger', amount: '0.033 ETH', status: 'Confirmed' },
  { id: 'TX-40826', block: 9842131, sender: 'District Hub', receiver: 'National Ledger', amount: '0.047 ETH', status: 'Queued' },
]

const adminStats = [
  { label: 'Live validators', value: '27 / 30' },
  { label: 'Voter checks', value: '99.97%' },
  { label: 'System uptime', value: '99.99%' },
  { label: 'Queue depth', value: '103 txs' },
]

const initialVoteLedgerRecords = [
  { state: 'Tamil Nadu', district: 'Chennai', party: 'TVK', voter: 'VOT-00149', type: 'CM', timestamp: '2026-08-20T08:15:00+05:30' },
  { state: 'Tamil Nadu', district: 'Coimbatore', party: 'TVK', voter: 'VOT-00462', type: 'CM', timestamp: '2026-08-20T08:32:00+05:30' },
  { state: 'Tamil Nadu', district: 'Madurai', party: 'DMK', voter: 'VOT-00813', type: 'CM', timestamp: '2026-08-20T09:05:00+05:30' },
  { state: 'Kerala', district: 'Thiruvananthapuram', party: 'CPI(M)', voter: 'VOT-01274', type: 'CM', timestamp: '2026-08-20T09:42:00+05:30' },
  { state: 'Maharashtra', district: 'Mumbai City', party: 'BJP', voter: 'VOT-02018', type: 'PM', timestamp: '2026-08-20T10:18:00+05:30' },
  { state: 'Uttar Pradesh', district: 'Lucknow', party: 'BJP', voter: 'VOT-02531', type: 'PM', timestamp: '2026-08-20T10:46:00+05:30' },
  { state: 'West Bengal', district: 'Kolkata', party: 'TMC', voter: 'VOT-03094', type: 'PM', timestamp: '2026-08-20T11:20:00+05:30' },
  { state: 'Delhi', district: 'New Delhi', party: 'AAP', voter: 'VOT-03510', type: 'PM', timestamp: '2026-08-20T11:58:00+05:30' },
]

const timelineItems = [
  { step: '01', title: 'Identity verification', detail: 'Voter identity and Aadhaar validation are completed in the district registry.' },
  { step: '02', title: 'Token issuance', detail: 'A one-time ballot token is generated and bound to the secure voter wallet.' },
  { step: '03', title: 'Vote sealed', detail: 'Encrypted ballots are committed to the chain and mirrored across the validator network.' },
  { step: '04', title: 'Audit release', detail: 'Public transparency reports are published without exposing private voter information.' },
]

const indiaElectionHistory = [
  { year: '1951-52', title: 'First Lok Sabha election', detail: 'India held its first general election after independence. The Indian National Congress formed the first Union government under Jawaharlal Nehru.' },
  { year: '1957', title: 'Second general election', detail: 'The second Lok Sabha election strengthened the parliamentary system and returned the Congress government.' },
  { year: '1962', title: 'Third general election', detail: 'The third general election continued India\'s first-past-the-post parliamentary tradition.' },
  { year: '1967', title: 'Fourth general election', detail: 'The election marked a major shift: Congress lost power in several states and coalition politics expanded.' },
  { year: '1971', title: 'Fifth general election', detail: 'The national election was held early and returned Indira Gandhi\'s government with a strong mandate.' },
  { year: '1975-77', title: 'Emergency and restoration of elections', detail: 'The Emergency period was followed by the 1977 general election, when the Janata Party formed the first non-Congress Union government.' },
  { year: '1980', title: 'Sixth general election', detail: 'The electorate returned Indira Gandhi and the Congress to national government.' },
  { year: '1984', title: 'Eighth general election', detail: 'After the assassination of Indira Gandhi, Rajiv Gandhi led Congress to a historic parliamentary majority.' },
  { year: '1989', title: 'Coalition era begins', detail: 'The ninth Lok Sabha election brought the National Front to power and made coalition governments central to national politics.' },
  { year: '1991', title: 'Tenth general election', detail: 'The election took place in phases amid extraordinary security conditions; P. V. Narasimha Rao later led the Union government.' },
  { year: '1996', title: 'Hung Lok Sabha', detail: 'No party secured a majority. The country saw short-lived governments before the United Front period.' },
  { year: '1998', title: 'Twelfth general election', detail: 'The BJP-led coalition formed the Union government, but it did not complete a full term.' },
  { year: '1999', title: 'Thirteenth general election', detail: 'The National Democratic Alliance formed a stable coalition government under Atal Bihari Vajpayee.' },
  { year: '2004', title: 'United Progressive Alliance', detail: 'The Congress-led UPA formed the Union government after the fourteenth Lok Sabha election.' },
  { year: '2009', title: 'UPA returns', detail: 'The fifteenth Lok Sabha election returned the UPA government for a second term.' },
  { year: '2014', title: 'BJP majority government', detail: 'The sixteenth Lok Sabha election produced the first single-party majority in three decades, with Narendra Modi as Prime Minister.' },
  { year: '2019', title: 'Seventeenth general election', detail: 'The BJP-led NDA returned to power with a larger majority in the seventeenth Lok Sabha.' },
  { year: '2024', title: 'Eighteenth general election', detail: 'The BJP-led NDA formed the Union government after the eighteenth Lok Sabha election; the Election Commission conducted voting in seven phases.' },
  { year: '2026', title: 'Current reference year', detail: 'This app is a civic technology demo. No official 2026 Lok Sabha result is represented here; future election data should be added only from Election Commission publications.' },
]

function stableHash(value) {
  let hash = 0
  for (let i = 0; i < value.length; i += 1) {
    hash = value.charCodeAt(i) + ((hash << 5) - hash)
  }
  return Math.abs(hash)
}

function createBlockHash(record, previousHash, blockNumber) {
  const payload = [
    blockNumber,
    previousHash,
    record.timestamp,
    record.state,
    record.district,
    record.party,
    record.voter,
    record.type,
  ].join('|')
  return `BLK-${stableHash(payload).toString(16).padStart(8, '0').toUpperCase()}`
}

function buildVoteChain(records) {
  return records.map((record, index) => {
    const previousHash = index === 0 ? 'GENESIS' : records[index - 1].blockHash
    return {
      ...record,
      blockNumber: index + 1,
      previousHash,
      blockHash: createBlockHash(record, previousHash, index + 1),
      integrity: 'Verified',
    }
  })
}

function getStatePartyOptions(stateName, type = 'cm') {
  if (type === 'pm') {
    return nationalPmParties
  }

  return stateParties[stateName] ?? defaultParties
}

function getPreferredPartyForState(stateName, districtName = '', type = 'pm') {
  if (type === 'cm' && stateName === 'Tamil Nadu') {
    const leader = tamilNaduCMDistrictLeaders[districtName] ?? 'C. Joseph Vijay'
    if (leader === 'C. Joseph Vijay') return 'TVK'
    if (leader === 'M. K. Stalin') return 'DMK'
    if (leader === 'Edappadi K. Palaniswami') return 'AIADMK'
    return 'DMK'
  }

  return getStatePartyOptions(stateName)[0] ?? 'Independent'
}

function buildCandidates(stateName, districtName, type) {
  const pmNames = ['Narendra Modi', 'Rahul Gandhi', 'Arvind Kejriwal', 'Mamata Banerjee', 'Amit Shah']
  const cmNames = ['M K Stalin', 'Yogi Adityanath', 'Pinarayi Vijayan', 'Siddaramaiah', 'N. Chandrababu Naidu']
  const isTamilNaduChiefMinisterProjection = type === 'cm' && stateName === 'Tamil Nadu'

  let names = type === 'pm' ? pmNames : cmNames
  if (isTamilNaduChiefMinisterProjection) {
    const districtLeader = tamilNaduCMDistrictLeaders[districtName] ?? 'C. Joseph Vijay'
    const baseNames = ['C. Joseph Vijay', 'M. K. Stalin', 'Edappadi K. Palaniswami', 'P. C. Kalyani', 'A. V. Velu']
    names = [districtLeader, ...baseNames.filter((name) => name !== districtLeader)]
  }

  const partyList = getStatePartyOptions(stateName)

  return names.map((name, index) => {
    const seed = `${stateName}-${districtName}-${type}-${name}`
    const isLeadingCandidate = isTamilNaduChiefMinisterProjection
      ? name === (tamilNaduCMDistrictLeaders[districtName] ?? 'C. Joseph Vijay')
      : false
    const base = isLeadingCandidate
      ? 710000 + (stableHash(seed) % 170000)
      : 260000 + (stableHash(seed) % 420000)
    const party = isTamilNaduChiefMinisterProjection && isLeadingCandidate
      ? (name === 'C. Joseph Vijay' ? 'TVK' : name === 'M. K. Stalin' ? 'DMK' : name === 'Edappadi K. Palaniswami' ? 'AIADMK' : 'Independent')
      : partyList[(stableHash(seed) + index) % partyList.length]

    return {
      id: index + 1,
      initials: name.split(' ').map((part) => part[0]).join('').slice(0, 2).toUpperCase(),
      name,
      party,
      color: palette[index % palette.length],
      votes: base + index * 26000,
      trend: isLeadingCandidate ? '+12.4%' : `+${((index + 1) * 0.8).toFixed(1)}%`,
    }
  })
}

function App() {
  const [page, setPage] = useState('dashboard')
  const [selectedState, setSelectedState] = useState('Tamil Nadu')
  const [selectedDistrict, setSelectedDistrict] = useState('Chennai')
  const [selectedThoguthi, setSelectedThoguthi] = useState(tamilNaduThoguthiCatalog.Chennai[0])
  const [resultType, setResultType] = useState('pm')
  const [selectedParty, setSelectedParty] = useState('DMK')
  const [ballotStatus, setBallotStatus] = useState('Ready to secure your vote.')
  const [loggedIn, setLoggedIn] = useState(false)
  const [loginData, setLoginData] = useState({ username: '', password: '' })
  const [loginMode, setLoginMode] = useState('voter')
  const [loginError, setLoginError] = useState('')
  const [publishedResults, setPublishedResults] = useState(false)
  const [galleryOpen, setGalleryOpen] = useState(false)
  const [txFilter, setTxFilter] = useState('all')
  const [voterLoggedIn, setVoterLoggedIn] = useState(false)
  const [voterLoginData, setVoterLoginData] = useState({ username: '', password: '' })
  const [voterVerification, setVoterVerification] = useState({ aadhaar: '', voterId: '' })
  const [voterValidated, setVoterValidated] = useState(false)
  const [voterLoginError, setVoterLoginError] = useState('')
  const [voterRegistry, setVoterRegistry] = useState([
    { name: 'Demo Voter', aadhaar: '123456789012', voterId: 'VOT-00149', state: 'Tamil Nadu', district: 'Chennai' },
    { name: 'Riya Sharma', aadhaar: '234567890123', voterId: 'VOT-00462', state: 'Tamil Nadu', district: 'Coimbatore' },
    { name: 'Arjun Nair', aadhaar: '345678901234', voterId: 'VOT-00813', state: 'Kerala', district: 'Thiruvananthapuram' },
  ])
  const [newVoter, setNewVoter] = useState({ name: '', aadhaar: '', voterId: '', state: 'Tamil Nadu', district: 'Chennai' })
  const [registrationFeedback, setRegistrationFeedback] = useState('')
  const [voteLedgerRecords, setVoteLedgerRecords] = useState(() => buildVoteChain(initialVoteLedgerRecords))

  const districtOptions = districtCatalog[selectedState] ?? []
  const thoguthiOptions = selectedState === 'Tamil Nadu'
    ? (tamilNaduThoguthiCatalog[selectedDistrict] ?? [])
    : []
  const partyOptions = useMemo(() => getStatePartyOptions(selectedState, resultType), [selectedState, resultType])

  const candidates = useMemo(
    () => buildCandidates(selectedState, selectedDistrict, resultType),
    [selectedState, selectedDistrict, resultType],
  )

  const totalVotes = useMemo(
    () => candidates.reduce((sum, candidate) => sum + candidate.votes, 0),
    [candidates],
  )

  const leading = candidates.reduce((winner, candidate) => (candidate.votes > winner.votes ? candidate : winner), candidates[0])
  const districtLeaderName = selectedState === 'Tamil Nadu' && resultType === 'cm'
    ? (tamilNaduCMDistrictLeaders[selectedDistrict] ?? 'C. Joseph Vijay')
    : leading.name
  const visibleLeadingCandidate = {
    ...leading,
    name: districtLeaderName,
    party: selectedState === 'Tamil Nadu' && resultType === 'cm'
      ? (tamilNaduDistrictPartyMap[selectedDistrict] ?? 'TVK')
      : leading.party,
  }
  const leadingShare = ((leading.votes / totalVotes) * 100).toFixed(1)
  const voteTurnout = (62 + (stableHash(`${selectedState}-${selectedDistrict}`) % 28)) / 1

  const resultPulse = candidates
    .map((candidate) => ({
      party: candidate.party,
      percent: Number(((candidate.votes / totalVotes) * 100).toFixed(1)),
      color: candidate.color,
    }))
    .sort((a, b) => {
      if (selectedState === 'Tamil Nadu' && resultType === 'cm') {
        if (a.party === 'TVK' && b.party !== 'TVK') return -1
        if (a.party !== 'TVK' && b.party === 'TVK') return 1
      }
      return b.percent - a.percent
    })

  const filteredTransactions = topTransactionRecords.filter((tx) => {
    if (txFilter === 'all') return true
    return tx.status.toLowerCase() === txFilter
  })

  const chronologicalVoteRecords = useMemo(
    () => [...voteLedgerRecords].sort((firstVote, secondVote) => new Date(firstVote.timestamp) - new Date(secondVote.timestamp)),
    [voteLedgerRecords],
  )
  const voteChainHealthy = voteLedgerRecords.every((vote, index) => {
    const previousHash = index === 0 ? 'GENESIS' : voteLedgerRecords[index - 1].blockHash
    return vote.previousHash === previousHash && vote.blockHash === createBlockHash(vote, previousHash, vote.blockNumber)
  })

  const liveVoteCount = useMemo(() => {
    const totals = {}
    voteLedgerRecords.forEach((vote) => {
      totals[vote.party] = (totals[vote.party] ?? 0) + 1
    })
    return Object.entries(totals).sort((a, b) => b[1] - a[1])
  }, [voteLedgerRecords])

  const handleStateChange = (stateName) => {
    const nextStateOptions = getStatePartyOptions(stateName, resultType)
    const nextDistrict = districtCatalog[stateName][0]
    const nextThoguthi = stateName === 'Tamil Nadu' ? tamilNaduThoguthiCatalog[nextDistrict][0] : ''
    const nextParty = resultType === 'cm' && stateName === 'Tamil Nadu'
      ? (tamilNaduDistrictPartyMap[nextDistrict] ?? getPreferredPartyForState(stateName, nextDistrict, resultType))
      : nextStateOptions[0]

    setSelectedState(stateName)
    setSelectedDistrict(nextDistrict)
    setSelectedThoguthi(nextThoguthi)
    setSelectedParty(nextParty)
    setBallotStatus(stateName === 'Tamil Nadu' && resultType === 'cm'
      ? `${tamilNaduCMDistrictLeaders[nextDistrict] ?? 'C. Joseph Vijay'} is leading in ${nextDistrict}.`
      : `Ready to vote in ${stateName}.`)
  }

  const handleElectionTypeChange = (nextType) => {
    setResultType(nextType)

    if (nextType === 'cm' && selectedState === 'Tamil Nadu') {
      const nextParty = tamilNaduDistrictPartyMap[selectedDistrict] ?? getPreferredPartyForState(selectedState, selectedDistrict, nextType)
      setSelectedParty(nextParty)
      setBallotStatus(`${tamilNaduCMDistrictLeaders[selectedDistrict] ?? 'C. Joseph Vijay'} is leading in ${selectedDistrict}.`)
      return
    }

    const nextStateOptions = getStatePartyOptions(selectedState, nextType)
    setSelectedParty(nextStateOptions[0])
    setBallotStatus(`Ready to vote in ${selectedState}.`)
  }

  const handleVoteCast = () => {
    if (!voterLoggedIn) {
      setBallotStatus('Please log in with your Aadhaar or Voter ID before casting a vote.')
      return
    }

    if (!voterValidated) {
      setBallotStatus('Complete Aadhaar and Voter ID verification before casting your vote.')
      return
    }

    if (selectedState === 'Tamil Nadu' && selectedParty === 'TVK' && resultType === 'cm') {
      setBallotStatus('Demo result projection: C. Joseph Vijay leads the Tamil Nadu CM fixture.')
      return
    }

    setBallotStatus(`Your vote for ${selectedParty} in ${selectedState} has been secured in the blockchain ledger.`)
    setVoterLoggedIn(false)
    setVoterValidated(false)
    setVoterLoginData({ username: '', password: '' })
    setVoterVerification({ aadhaar: '', voterId: '' })
  }

  const handleVoterLogin = (event) => {
    event.preventDefault()
    const normalizedUsername = voterLoginData.username.trim().replace(/\s+/g, '')
    const password = voterLoginData.password.trim()

    const isValidUsername = /^\d{12}$/.test(normalizedUsername) || /^VOT-\d{5,8}$/i.test(normalizedUsername)

    if (isValidUsername && password.length > 0) {
      setVoterLoggedIn(true)
      setVoterValidated(false)
      setVoterLoginError('')
      return
    }

    setVoterLoginError('Use valid Aadhaar number or Voter ID and any non-empty password.')
    setVoterLoggedIn(false)
  }

  const handleVoterVoteValidation = () => {
    const matchingRecord = getVoterMatch({
      username: voterLoginData.username,
      aadhaar: voterVerification.aadhaar,
      voterId: voterVerification.voterId,
      registry: [...voterRegistry, ...validVoterRecords],
    })

    if (!matchingRecord) {
      setBallotStatus('Verification failed. Aadhaar and Voter ID do not match the registered voter profile.')
      setVoterValidated(false)
      return
    }

    const newEntry = {
      state: selectedState,
      district: selectedDistrict,
      party: selectedParty,
      voter: matchingRecord.voterId,
      type: resultType === 'pm' ? 'PM' : 'CM',
      timestamp: new Date().toISOString(),
    }

    setVoteLedgerRecords((prev) => buildVoteChain([...prev, newEntry]))
    setVoterValidated(true)
    setVoterLoggedIn(true)
    setVoterLoginData({ username: '', password: '' })
    setVoterVerification({ aadhaar: '', voterId: '' })
    setBallotStatus(`Vote validated and stored in the blockchain ledger for ${selectedState} / ${selectedDistrict}.`)
  }

  const handleVoterRegistration = (event) => {
    event.preventDefault()

    if (!newVoter.name.trim() || !/^\d{12}$/.test(newVoter.aadhaar.trim()) || !/^VOT-\d{5,8}$/i.test(newVoter.voterId.trim())) {
      setRegistrationFeedback('Use a valid name, 12-digit Aadhaar, and Voter ID format such as VOT-00149.')
      return
    }

    const duplicate = [...voterRegistry, ...validVoterRecords].some((record) =>
      record.aadhaar === newVoter.aadhaar.trim() || record.voterId?.toUpperCase() === newVoter.voterId.trim().toUpperCase()
    )

    if (duplicate) {
      setRegistrationFeedback('This voter is already registered and cannot vote twice.')
      return
    }

    const enrolled = {
      name: newVoter.name.trim(),
      aadhaar: newVoter.aadhaar.trim(),
      voterId: newVoter.voterId.trim().toUpperCase(),
      state: newVoter.state,
      district: newVoter.district,
    }

    setVoterRegistry((prev) => [...prev, enrolled])
    setNewVoter({ name: '', aadhaar: '', voterId: '', state: 'Tamil Nadu', district: 'Chennai' })
    setRegistrationFeedback(`Voter registration complete for ${enrolled.name}. They are now eligible to cast one ballot.`)
  }

  const handleLogin = (event) => {
    event.preventDefault()
    const username = loginData.username.trim()
    const password = loginData.password.trim()

    const isAdminLogin = loginMode === 'admin'
    const isValidLogin = isAdminLogin
      ? username === 'election' && password === 'india123'
      : username.length > 0 && password.length > 0

    if (isValidLogin) {
      setLoggedIn(true)
      setLoginError('')
      setPublishedResults(false)
      setPage(isAdminLogin ? 'admin' : 'dashboard')
      return
    }

    setLoginError(isAdminLogin
      ? 'Invalid admin credentials. Use election / india123.'
      : 'Enter a username and password to continue.')
    setLoggedIn(false)
  }

  const handleLaunchSecureVote = () => {
    setResultType('cm')
    if (selectedState === 'Tamil Nadu') {
      setSelectedParty('TVK')
      setBallotStatus('TVK is leading in Tamil Nadu for the Chief Minister election.')
    }
    setPage('results')
  }

  const handleReviewAuditTrail = () => {
    setTxFilter('all')
    setPage('transactions')
  }

  const handleHistoryOpen = () => {
    setPage('history')
  }

  const handlePublishResults = () => {
    setPublishedResults(true)
    setPage('dashboard')
    setBallotStatus('Election results published and visible on the dashboard.')
  }

  const handleLogout = () => {
    setLoggedIn(false)
    setLoginError('')
    setPublishedResults(false)
    setPage('admin')
  }

  return (
    <>
      {!loggedIn ? (
        <main className="login-screen">
          <div className="parliament-backdrop" role="img" aria-label="Red Fort in Delhi" />
          <div className="login-orbit orbit-one" />
          <div className="login-orbit orbit-two" />
          <div className="login-visual">
            <span className="status-pill">India election stack</span>
            <div className="login-flag-stage" aria-label="Indian national flag">
              <span className="flag-pole" />
              <div className="login-flag">
                <span className="flag-saffron" />
                <span className="flag-white"><i>☸</i></span>
                <span className="flag-green" />
              </div>
              <span className="flag-glow" />
            </div>
            <h1>Every vote deserves a visible chain of trust.</h1>
            <p>Sign in to explore district results, constituency data, and your secure voting dashboard.</p>
            <div className="login-signal"><span /><span /><span /><span /><span /></div>
            <div className="heritage-strip" aria-label="Indian heritage and democracy highlights">
              <div className="heritage-tile flag-tile"><strong>🇮🇳</strong><span>Tricolour</span></div>
              <div className="heritage-tile rupee-tile"><strong>₹</strong><span>Jan Dhan</span></div>
              <div className="heritage-tile history-tile"><strong>1947</strong><span>Freedom</span></div>
              <div className="heritage-tile politics-tile"><strong>☸</strong><span>Lok Sabha</span></div>
              <div className="heritage-tile leader-tile"><strong>✦</strong><span>Voices of India</span></div>
            </div>
          </div>
          <section className="panel login-box login-screen-box">
            <div className="brand-wrap login-brand">
                <div className="brand-mark"><span>B</span><i className="brand-wheel">☸</i></div>
              <div><p className="eyebrow">Digital voter service</p><h2>BlockVote India</h2></div>
            </div>
            <div className="login-mode-switch" role="tablist" aria-label="Choose login type">
              <button type="button" role="tab" aria-selected={loginMode === 'voter'} className={loginMode === 'voter' ? 'login-mode active' : 'login-mode'} onClick={() => { setLoginMode('voter'); setLoginError('') }}>Voter login</button>
              <button type="button" role="tab" aria-selected={loginMode === 'admin'} className={loginMode === 'admin' ? 'login-mode active' : 'login-mode'} onClick={() => { setLoginMode('admin'); setLoginError('') }}>Admin login</button>
            </div>
            <div className="panel-header login-heading"><div><span className="section-tag">{loginMode === 'admin' ? 'Admin access' : 'Voter access'}</span><h3>{loginMode === 'admin' ? 'Control room sign in' : 'Welcome back'}</h3></div><span>Secure session</span></div>
            <form onSubmit={handleLogin} className="login-form">
              <label><span>{loginMode === 'admin' ? 'Admin username' : 'Voter username'}</span><input autoFocus type="text" value={loginData.username} onChange={(event) => setLoginData({ ...loginData, username: event.target.value })} placeholder={loginMode === 'admin' ? 'election' : 'your username'} /></label>
              <label><span>Password</span><input type="password" value={loginData.password} onChange={(event) => setLoginData({ ...loginData, password: event.target.value })} placeholder={loginMode === 'admin' ? 'india123' : 'your password'} /></label>
              {loginError && <div className="login-error">{loginError}</div>}
              <button type="submit" className="primary-button full-width">{loginMode === 'admin' ? 'Enter control room' : 'Continue to dashboard'}</button>
            </form>
            <p className="login-caption">{loginMode === 'admin' ? 'Admin demo: election / india123' : 'Use any username and password to enter the demo dashboard.'}</p>
            <div className="heritage-gallery login-freedom-gallery">
              <div className="gallery-heading"><span>Freedom archive</span><strong>India in focus</strong></div>
              <div className="gallery-section-label">Freedom fighters</div>
              <div className="freedom-gallery">
                <figure><div className="portrait-frame"><img src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Portrait_Gandhi.jpg" alt="Mahatma Gandhi" onError={(event) => event.currentTarget.classList.add('image-failed')} /><span>MG</span></div><figcaption>Mahatma Gandhi</figcaption></figure>
                <figure><div className="portrait-frame"><img src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Bhagat_Singh_1929.jpg" alt="Bhagat Singh" onError={(event) => event.currentTarget.classList.add('image-failed')} /><span>BS</span></div><figcaption>Bhagat Singh</figcaption></figure>
                <figure><div className="portrait-frame"><img src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Subhas_Chandra_Bose_NRB.jpg" alt="Subhas Chandra Bose" onError={(event) => event.currentTarget.classList.add('image-failed')} /><span>SCB</span></div><figcaption>Subhas Bose</figcaption></figure>
              </div>
            </div>
          </section>
        </main>
      ) : (
      <>
      <header className="topbar">
        <div className="brand-wrap">
          <div className="brand-mark"><span>B</span><i className="brand-wheel">☸</i></div>
          <div>
            <p className="eyebrow">India election stack</p>
            <h2>BlockVote India</h2>
          </div>
        </div>

        <nav className="nav">
          <button type="button" className={page === 'dashboard' ? 'nav-link active' : 'nav-link'} onClick={() => setPage('dashboard')}>Overview</button>
          <button type="button" className={page === 'results' ? 'nav-link active' : 'nav-link'} onClick={() => setPage('results')}>Results</button>
          <button type="button" className={page === 'transactions' ? 'nav-link active' : 'nav-link'} onClick={() => setPage('transactions')}>Transactions</button>
          <button type="button" className={page === 'history' ? 'nav-link active' : 'nav-link'} onClick={handleHistoryOpen}>India history</button>
          <button type="button" className={page === 'admin' ? 'nav-link active' : 'nav-link'} onClick={() => setPage('admin')}>Admin</button>
        </nav>

        <div className="topbar-actions">
          <span className="election-badge">{resultType === 'pm' ? 'PM Election' : 'CM Election'}</span>
          {!loggedIn ? (
            <button type="button" className="ghost-button" onClick={() => setPage('admin')}>Control room</button>
          ) : (
            <button type="button" className="ghost-button" onClick={handleLogout}>Logout</button>
          )}
        </div>
      </header>

      <main className="app-shell">
        {page === 'dashboard' && (
          <>
            <section className="hero">
              <div className="hero-copy">
                <span className="status-pill">National electoral blockchain</span>
                <h1>Secure e-voting infrastructure for every Indian state and constituency.</h1>
                <p>
                  Designed for Prime Minister and Chief Minister elections, this blockchain-backed voting platform brings end-to-end security, transparency, district mapping, and public trust to every ballot.
                </p>
                <div className="hero-actions">
                  <button type="button" className="primary-button" onClick={handleLaunchSecureVote}>Launch secure vote</button>
                  <button type="button" className="secondary-button" onClick={handleReviewAuditTrail}>Review audit trail</button>
                  <button type="button" className="gallery-button" onClick={() => setGalleryOpen(true)}>View civic gallery</button>
                </div>
                <div className="hero-metrics">
                  <div className="mini-stat"><p>Registered voters</p><strong>930M</strong><span>+2.7%</span></div>
                  <div className="mini-stat"><p>Verified IDs</p><strong>99.97%</strong><span>+0.06%</span></div>
                  <div className="mini-stat"><p>Block latency</p><strong>24ms</strong><span>Fast</span></div>
                  <div className="mini-stat"><p>Votes secured</p><strong>3.2B</strong><span>Immutable</span></div>
                </div>
              </div>

              <div className="hero-panel">
                <div className="panel-header compact">
                  <span>National network</span>
                  <span className="live-dot">Live</span>
                </div>
                <div className="national-emblem-row">
                  <div className="indian-flag" aria-label="Indian tricolour flag">
                    <span className="flag-saffron" /><span className="flag-white"><i>☸</i></span><span className="flag-green" />
                  </div>
                  <div className="civic-caption"><strong>भारत · INDIA</strong><span>One nation · one secure ledger</span></div>
                </div>
                <div className="map-node-grid">
                  <span className="node node-a">Delhi</span>
                  <span className="node node-b">Mumbai</span>
                  <span className="node node-c">Kolkata</span>
                  <span className="node node-d">Bengaluru</span>
                  <span className="node node-e">Chennai</span>
                </div>
                <div className="ledger-card">
                  <div><p className="ledger-label">Current block</p><strong>9,842,119</strong></div>
                  <div className="rupee-ledger"><p className="ledger-label">Vote value secured</p><strong>₹ 3.2B</strong><span className="coin coin-one">₹</span><span className="coin coin-two">₹</span></div>
                </div>
              </div>
            </section>

            <section className="panel state-panel">
              <div className="panel-header">
                <h3>State and district coverage</h3>
                <span>{stateOptions.length} states & UTs mapped · demo result fixture</span>
              </div>
              <div className="selector-grid">
                <label>
                  <span>State</span>
                  <select value={selectedState} onChange={(event) => handleStateChange(event.target.value)}>
                    {stateOptions.map((stateName) => <option key={stateName} value={stateName}>{stateName}</option>)}
                  </select>
                </label>
                <label>
                  <span>District</span>
                  <select value={selectedDistrict} onChange={(event) => {
                    const nextDistrict = event.target.value
                    setSelectedDistrict(nextDistrict)
                    if (selectedState === 'Tamil Nadu') setSelectedThoguthi(tamilNaduThoguthiCatalog[nextDistrict][0])
                    if (selectedState === 'Tamil Nadu' && resultType === 'cm') {
                      const nextParty = tamilNaduDistrictPartyMap[nextDistrict] ?? getPreferredPartyForState(selectedState, nextDistrict, resultType)
                      setSelectedParty(nextParty)
                      setBallotStatus(`${tamilNaduCMDistrictLeaders[nextDistrict] ?? 'C. Joseph Vijay'} is leading in ${nextDistrict}.`)
                    }
                  }}>
                    {districtOptions.map((district) => <option key={district} value={district}>{district}</option>)}
                  </select>
                </label>
                {selectedState === 'Tamil Nadu' && <label>
                  <span>Thoguthi</span>
                  <select value={selectedThoguthi} onChange={(event) => setSelectedThoguthi(event.target.value)}>
                    {thoguthiOptions.map((thoguthi) => <option key={thoguthi} value={thoguthi}>{thoguthi}</option>)}
                  </select>
                </label>}
              </div>
              <div className="coverage-metrics">
                <div className="metric-item"><span>State</span><strong>{selectedState}</strong></div>
                <div className="metric-item"><span>District</span><strong>{selectedDistrict}</strong></div>
                <div className="metric-item"><span>Turnout</span><strong>{voteTurnout.toFixed(1)}%</strong></div>
                <div className="metric-item"><span>Verified votes</span><strong>{(1000000 + stableHash(selectedDistrict) % 400000).toLocaleString('en-IN')}</strong></div>
              </div>

              <div className="ballot-panel">
                <div className="panel-header ballot-header">
                  <div>
                    <span className="section-tag">Ballot</span>
                    <h3>Select election and party</h3>
                  </div>
                </div>

                {!voterLoggedIn ? (
                  <div className="voter-auth-box">
                    <form onSubmit={handleVoterLogin} className="voter-auth-form">
                      <label>
                        <span>Voter ID or Aadhaar</span>
                        <input
                          type="text"
                          value={voterLoginData.username}
                          onChange={(event) => setVoterLoginData({ ...voterLoginData, username: event.target.value })}
                          placeholder="e.g. 123456789012 or VOT-00149"
                        />
                      </label>
                      <label>
                        <span>Password</span>
                        <input
                          type="password"
                          value={voterLoginData.password}
                          onChange={(event) => setVoterLoginData({ ...voterLoginData, password: event.target.value })}
                          placeholder="Any password"
                        />
                      </label>
                      {voterLoginError && <p className="login-error">{voterLoginError}</p>}
                      <button type="submit" className="primary-button full-width">Login to vote</button>
                    </form>
                  </div>
                ) : (
                  <>
                    <div className="voter-auth-box">
                      <div className="voter-auth-form">
                        <label>
                          <span>Aadhaar card</span>
                          <input
                            type="text"
                            value={voterVerification.aadhaar}
                            onChange={(event) => setVoterVerification({ ...voterVerification, aadhaar: event.target.value })}
                            placeholder="12-digit Aadhaar number"
                          />
                        </label>
                        <label>
                          <span>Voter ID</span>
                          <input
                            type="text"
                            value={voterVerification.voterId}
                            onChange={(event) => setVoterVerification({ ...voterVerification, voterId: event.target.value })}
                            placeholder="VOT-00149"
                          />
                        </label>
                        <button type="button" className="primary-button full-width" onClick={handleVoterVoteValidation}>Validate and store vote</button>
                      </div>
                    </div>

                    <div className="ballot-form">
                      <div className="ballot-mode-block">
                        <span>Election type</span>
                        <div className="mode-toggle compact-mode-toggle">
                          <button type="button" className={resultType === 'pm' ? 'mode-button active' : 'mode-button'} onClick={() => handleElectionTypeChange('pm')}>PM Election</button>
                          <button type="button" className={resultType === 'cm' ? 'mode-button active' : 'mode-button'} onClick={() => handleElectionTypeChange('cm')}>CM Election</button>
                        </div>
                      </div>
                      <label>
                        <span>Choose party</span>
                        <select value={selectedParty} onChange={(event) => {
                          setSelectedParty(event.target.value)
                          if (selectedState === 'Tamil Nadu' && event.target.value === 'TVK' && resultType === 'cm') {
                            setBallotStatus('Demo result projection: C. Joseph Vijay leads the Tamil Nadu CM fixture.')
                          } else {
                            setBallotStatus(`Ready to vote in ${selectedState}.`)
                          }
                        }}>
                          {partyOptions.map((partyName) => (
                            <option key={partyName} value={partyName}>{partyName}</option>
                          ))}
                        </select>
                      </label>
                      <button type="button" className="primary-button" onClick={handleVoteCast}>Cast vote</button>
                    </div>
                  </>
                )}
                <p className="ballot-status">{ballotStatus}</p>
              </div>
              {publishedResults && selectedState === 'Tamil Nadu' && <div className="winner-reveal" key={`${selectedDistrict}-${selectedThoguthi}`}>
                <span className="winner-kicker">Published district result</span>
                <strong>C.JOSEPH VIJAY</strong>
                <span>TVK · Winner in {selectedDistrict}</span>
                <i>Result verified on the public ledger</i>
              </div>}
            </section>

            <section className="panel">
              <div className="panel-header">
                <div>
                  <span className="section-tag">Election system</span>
                  <h3>Core voting workflow</h3>
                </div>
              </div>
              <div className="feature-grid">
                {featureChecklist.map((feature) => (
                  <article key={feature.title} className="feature-card">
                    <div className="feature-icon">✓</div>
                    <h4>{feature.title}</h4>
                    <p>{feature.text}</p>
                  </article>
                ))}
              </div>
            </section>

            <section className="panel">
              <div className="panel-header">
                <div>
                  <span className="section-tag">Registration</span>
                  <h3>Voter registration and identity onboarding</h3>
                </div>
              </div>
              <form className="selector-grid" onSubmit={handleVoterRegistration}>
                <label>
                  <span>Full name</span>
                  <input value={newVoter.name} onChange={(event) => setNewVoter({ ...newVoter, name: event.target.value })} placeholder="Enter full name" />
                </label>
                <label>
                  <span>Aadhaar</span>
                  <input value={newVoter.aadhaar} onChange={(event) => setNewVoter({ ...newVoter, aadhaar: event.target.value })} placeholder="12-digit Aadhaar" />
                </label>
                <label>
                  <span>Voter ID</span>
                  <input value={newVoter.voterId} onChange={(event) => setNewVoter({ ...newVoter, voterId: event.target.value })} placeholder="VOT-00149" />
                </label>
                <label>
                  <span>State</span>
                  <select value={newVoter.state} onChange={(event) => setNewVoter({ ...newVoter, state: event.target.value })}>
                    {stateOptions.map((stateName) => <option key={stateName} value={stateName}>{stateName}</option>)}
                  </select>
                </label>
                <label>
                  <span>District</span>
                  <select value={newVoter.district} onChange={(event) => setNewVoter({ ...newVoter, district: event.target.value })}>
                    {(districtCatalog[newVoter.state] ?? []).map((districtName) => <option key={districtName} value={districtName}>{districtName}</option>)}
                  </select>
                </label>
                <div style={{ display: 'flex', alignItems: 'end' }}>
                  <button type="submit" className="primary-button full-width">Register voter</button>
                </div>
              </form>
              {registrationFeedback && <p className="ballot-status" style={{ color: '#8ff4bf' }}>{registrationFeedback}</p>}
            </section>

            <section className="feature-section">
              <div className="section-header">
                <span className="section-tag">Election assurance</span>
                <h3>Built for trust, transparency, and scale.</h3>
              </div>
              <div className="feature-grid">
                {electionHighlights.map((feature) => (
                  <article key={feature.title} className="feature-card">
                    <div className="feature-icon">{feature.icon}</div>
                    <h4>{feature.title}</h4>
                    <p>{feature.text}</p>
                  </article>
                ))}
              </div>
            </section>
            <section className="history-entry panel">
              <div><span className="section-tag">Civic archive</span><h3>Trace India&apos;s electoral journey</h3><p>Explore the major Lok Sabha elections and democratic turning points from 1951-52 through the current 2026 reference year.</p></div>
              <button type="button" className="primary-button" onClick={handleHistoryOpen}>Open India history</button>
            </section>
          </>
        )}

        {page === 'history' && (
          <section className="panel history-page">
            <div className="panel-header history-header">
              <div><span className="section-tag">Civic archive</span><h3>History of elections in India</h3><p>Major Lok Sabha elections and democratic milestones</p></div>
              <button type="button" className="secondary-button" onClick={() => setPage('dashboard')}>Back to dashboard</button>
            </div>
            <div className="history-notice"><strong>Reference note</strong><span>This is a curated educational timeline, not a complete official election database. Results through 2024 are historical context; 2026 is shown as the current reference year.</span></div>
            <div className="history-timeline">
              {indiaElectionHistory.map((item, index) => (
                <article className="history-event" key={item.year}>
                  <div className="history-year">{item.year}</div>
                  <div className="history-dot" />
                  <div className="history-event-copy"><span>Milestone {String(index + 1).padStart(2, '0')}</span><h4>{item.title}</h4><p>{item.detail}</p></div>
                </article>
              ))}
            </div>
          </section>
        )}

        {page === 'results' && (
          <section className="panel results-page">
            <div className="panel-header results-topbar">
              <div>
                <span className="section-tag">Result centre</span>
                <h3>India election result dashboard</h3>
              </div>
              <div className="mode-toggle">
                <button type="button" className={resultType === 'pm' ? 'mode-button active' : 'mode-button'} onClick={() => handleElectionTypeChange('pm')}>PM Election</button>
                <button type="button" className={resultType === 'cm' ? 'mode-button active' : 'mode-button'} onClick={() => handleElectionTypeChange('cm')}>CM Election</button>
              </div>
            </div>

            <div className="selector-grid double-grid">
              <label>
                <span>State</span>
                <select value={selectedState} onChange={(event) => handleStateChange(event.target.value)}>
                  {stateOptions.map((stateName) => <option key={stateName} value={stateName}>{stateName}</option>)}
                </select>
              </label>
              <label>
                <span>District</span>
                <select value={selectedDistrict} onChange={(event) => {
                  const nextDistrict = event.target.value
                  setSelectedDistrict(nextDistrict)
                    if (selectedState === 'Tamil Nadu') setSelectedThoguthi(tamilNaduThoguthiCatalog[nextDistrict][0])
                  if (selectedState === 'Tamil Nadu' && resultType === 'cm') {
                    const nextParty = tamilNaduDistrictPartyMap[nextDistrict] ?? getPreferredPartyForState(selectedState, nextDistrict, resultType)
                    setSelectedParty(nextParty)
                    setBallotStatus(`${tamilNaduCMDistrictLeaders[nextDistrict] ?? 'C. Joseph Vijay'} is leading in ${nextDistrict}.`)
                  }
                }}>
                  {districtOptions.map((district) => <option key={district} value={district}>{district}</option>)}
                </select>
              </label>
              {selectedState === 'Tamil Nadu' && <label>
                <span>Thoguthi</span>
                <select value={selectedThoguthi} onChange={(event) => setSelectedThoguthi(event.target.value)}>
                  {thoguthiOptions.map((thoguthi) => <option key={thoguthi} value={thoguthi}>{thoguthi}</option>)}
                </select>
              </label>}
            </div>

            <div className="result-stat-grid">
              <div className="mini-stat wide"><p>Leading candidate</p><strong>{visibleLeadingCandidate.name}</strong><span>{leadingShare}% vote share</span></div>
              <div className="mini-stat wide"><p>Contest</p><strong>{resultType === 'pm' ? 'Prime Minister' : 'Chief Minister'}</strong><span>{selectedState}</span></div>
              <div className="mini-stat wide"><p>Turnout</p><strong>{voteTurnout.toFixed(1)}%</strong><span>{selectedDistrict}</span></div>
            </div>
            {publishedResults && selectedState === 'Tamil Nadu' && <div className="winner-reveal winner-reveal-wide" key={`${selectedDistrict}-${selectedThoguthi}-result`}><span className="winner-kicker">Published result · {selectedThoguthi}</span><strong>C.JOSEPH VIJAY IS WON</strong><span>TVK · {selectedDistrict} district</span><i>Verified and published to the dashboard</i></div>}

            <div className="panel" style={{ padding: '18px 20px' }}>
              <div className="panel-header">
                <div>
                  <span className="section-tag">Real-time tally</span>
                  <h3>Live vote count</h3>
                </div>
              </div>
              <div className="results-list">
                {liveVoteCount.map(([party, count]) => (
                  <div key={party} className="result-item">
                    <div className="result-header"><span>{party}</span><strong>{count}</strong></div>
                    <div className="progress-bar small"><span style={{ width: `${Math.min((count / Math.max(voteLedgerRecords.length, 1)) * 100, 100)}%`, background: palette[(party.length + count) % palette.length] }} /></div>
                  </div>
                ))}
              </div>
            </div>

            <div className="result-layout">
              <div className="candidate-column">
                {candidates.map((candidate) => (
                  <div key={candidate.id} className="candidate-card result-card">
                    <div className="candidate-row">
                      <span className="avatar" style={{ background: candidate.color }}>{candidate.initials}</span>
                      <div>
                        <strong>{candidate.name}</strong>
                        <span>{candidate.party}</span>
                      </div>
                    </div>
                    <div className="candidate-meta">
                      <span>{candidate.votes.toLocaleString('en-IN')} votes</span>
                      <em>{candidate.trend}</em>
                    </div>
                    <div className="progress-bar small"><span style={{ width: `${(candidate.votes / totalVotes) * 100}%`, background: candidate.color }} /></div>
                  </div>
                ))}
              </div>

              <div className="results-panel">
                <div className="panel-header">
                  <h3>Vote pulse</h3>
                  <span>Updated 4 sec ago</span>
                </div>
                <div className="results-list">
                  {resultPulse.map((result) => (
                    <div key={`${result.party}-${result.percent}`} className="result-item">
                      <div className="result-header"><span>{result.party}</span><strong>{result.percent}%</strong></div>
                      <div className="progress-bar small"><span style={{ width: `${result.percent}%`, background: result.color }} /></div>
                    </div>
                  ))}
                </div>
                <div className="mini-summary">
                  <div>
                    <span>Polling booths</span>
                    <strong>{(252 + stableHash(selectedDistrict) % 440).toLocaleString('en-IN')}</strong>
                  </div>
                  <div>
                    <span>District verified</span>
                    <strong>{(98 + stableHash(selectedState) % 2).toFixed(1)}%</strong>
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}

        {page === 'transactions' && (
          <section className="panel transactions-page">
            <div className="panel-header transaction-header">
              <div>
                <h3>Blockchain transaction history</h3>
                <span>Immutable ledger</span>
              </div>
              <div className="transaction-toolbar">
                <button type="button" className={txFilter === 'all' ? 'filter-button active' : 'filter-button'} onClick={() => setTxFilter('all')}>All</button>
                <button type="button" className={txFilter === 'confirmed' ? 'filter-button active' : 'filter-button'} onClick={() => setTxFilter('confirmed')}>Confirmed</button>
                <button type="button" className={txFilter === 'pending' ? 'filter-button active' : 'filter-button'} onClick={() => setTxFilter('pending')}>Pending</button>
                <button type="button" className={txFilter === 'queued' ? 'filter-button active' : 'filter-button'} onClick={() => setTxFilter('queued')}>Queued</button>
              </div>
            </div>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr><th>Txn ID</th><th>Block</th><th>Sender</th><th>Receiver</th><th>Amount</th><th>Status</th></tr>
                </thead>
                <tbody>
                  {filteredTransactions.map((tx) => (
                    <tr key={tx.id}>
                      <td>{tx.id}</td>
                      <td>{tx.block}</td>
                      <td>{tx.sender}</td>
                      <td>{tx.receiver}</td>
                      <td>{tx.amount}</td>
                      <td><span className={`tx-status ${tx.status.toLowerCase()}`}>{tx.status}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {page === 'admin' && (
          <section className="admin-page">
            {!loggedIn ? (
              <div className="panel login-box">
                <div className="panel-header">
                  <h3>Secure admin login</h3>
                  <span>Protected access</span>
                </div>
                <form onSubmit={handleLogin} className="login-form">
                  <label><span>Username</span><input type="text" value={loginData.username} onChange={(event) => setLoginData({ ...loginData, username: event.target.value })} /></label>
                  <label><span>Password</span><input type="password" value={loginData.password} onChange={(event) => setLoginData({ ...loginData, password: event.target.value })} /></label>
                  <div className="secure-ledger-note">
                    <strong>Blockchain storage:</strong> every vote is encrypted, signed, hashed, and stored in the immutable ledger before it is published to the national audit trail.
                  </div>
                  {loginError && <div className="login-error">{loginError}</div>}
                  <button type="submit" className="primary-button full-width">Login to control room</button>
                </form>
              </div>
            ) : (
              <>
                <div className="panel admin-overview">
                  <div className="panel-header">
                    <h3>Election control room</h3>
                    <span>Admin authenticated</span>
                  </div>
                  <div className="admin-grid">
                    {adminStats.map((item) => (
                      <div key={item.label} className="metric-item"><span>{item.label}</span><strong>{item.value}</strong></div>
                    ))}
                  </div>
                </div>

                <div className="panel">
                  <div className="panel-header">
                    <h3>Smart contract status</h3>
                    <span>Election management rules</span>
                  </div>
                  <div className="results-list">
                    <div className="result-item"><div className="result-header"><span>registerVoter()</span><strong>Active</strong></div><div className="progress-bar small"><span style={{ width: '100%', background: '#3ddc97' }} /></div></div>
                    <div className="result-item"><div className="result-header"><span>validateBallot()</span><strong>Active</strong></div><div className="progress-bar small"><span style={{ width: '100%', background: '#3ca5ff' }} /></div></div>
                    <div className="result-item"><div className="result-header"><span>countVotes()</span><strong>Live</strong></div><div className="progress-bar small"><span style={{ width: '96%', background: '#ff7f3f' }} /></div></div>
                    <div className="result-item"><div className="result-header"><span>publishResult()</span><strong>Ready</strong></div><div className="progress-bar small"><span style={{ width: '88%', background: '#ffd36b' }} /></div></div>
                  </div>
                </div>

                <div className="panel">
                  <div className="panel-header">
                    <h3>Vote history</h3>
                    <span>Chronological order · oldest to newest · {voteChainHealthy ? 'chain verified' : 'integrity warning'}</span>
                  </div>
                  <div className="table-wrap">
                    <table>
                      <thead>
                        <tr><th>Block</th><th>Date and time</th><th>State</th><th>District</th><th>Party</th><th>Voter ID</th><th>Hash</th><th>Integrity</th></tr>
                      </thead>
                      <tbody>
                        {chronologicalVoteRecords.map((vote) => (
                          <tr key={`${vote.state}-${vote.district}-${vote.voter}-${vote.timestamp}`}>
                            <td>#{vote.blockNumber}</td>
                            <td>{new Date(vote.timestamp).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' })}</td>
                            <td>{vote.state}</td>
                            <td>{vote.district}</td>
                            <td>{vote.party}</td>
                            <td>{vote.voter}</td>
                            <td><code className="block-hash">{vote.blockHash}</code></td>
                            <td><span className="chain-status">{vote.integrity}</span></td>
                            <td>{vote.type}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  <div className="publish-actions">
                    <button type="button" className="primary-button" onClick={handlePublishResults}>Publish result</button>
                    {publishedResults && <span className="published-badge">Published to dashboard</span>}
                  </div>
                </div>
 
                <div className="admin-panels">
                  <div className="panel">
                    <div className="panel-header"><h3>Recent actions</h3><span>Audit trail</span></div>
                    <ul className="assurance-list">
                      <li><span className="checkmark">✓</span> Voter district credentials synced for 3,257 polling stations.</li>
                      <li><span className="checkmark">✓</span> Smart contract verification completed with 100% hash consistency.</li>
                      <li><span className="checkmark">✓</span> Network signature pool updated across 27 validator nodes.</li>
                      <li><span className="checkmark">✓</span> District-level audit file exported to the national transparency archive.</li>
                    </ul>
                  </div>
 
                  <div className="panel">
                    <div className="panel-header"><h3>Election lifecycle</h3><span>Live state</span></div>
                    <div className="timeline-list">
                      {timelineItems.map((item) => (
                        <div key={item.step} className="timeline-item">
                          <span className="timeline-step">{item.step}</span>
                          <div>
                            <h4>{item.title}</h4>
                            <p>{item.detail}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </>
            )}
          </section>
        )}
      </main>

      <footer className="footer">
        <p>Designed for India&apos;s digital democracy with blockchain-backed integrity, accessibility, and civic trust.</p>
      </footer>
      {galleryOpen && (
        <div className="gallery-modal-backdrop" role="presentation" onClick={() => setGalleryOpen(false)}>
          <section className="gallery-modal" role="dialog" aria-modal="true" aria-labelledby="gallery-title" onClick={(event) => event.stopPropagation()}>
            <div className="panel-header gallery-modal-header">
              <div><span className="section-tag">India in focus</span><h3 id="gallery-title">Civic landmarks</h3></div>
              <button type="button" className="modal-close" aria-label="Close civic gallery" onClick={() => setGalleryOpen(false)}>×</button>
            </div>
            <div className="popup-gallery-grid">
              <figure><img src="/taj-mahal.jpg" alt="Taj Mahal in Agra" /><figcaption><strong>Taj Mahal</strong><span>Agra · A symbol of Indian heritage</span></figcaption></figure>
              <figure><img src="/red-fort.jpg" alt="Red Fort in Delhi" /><figcaption><strong>Red Fort</strong><span>Delhi · A landmark of India&apos;s history</span></figcaption></figure>
            </div>
          </section>
        </div>
      )}
      </>
      )}
    </>
  )
}

export default App
