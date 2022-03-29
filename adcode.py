

#读取文件到行
#列表
#2020年最新记录http://www.mca.gov.cn/article/sj/xzqh/2020/20201201.html

lines = []
f = open('20201201.html')
lines = f.readlines()
f.close()

#取编码和名字
blocks = []

flag = False

total = len(lines)

for i in range(total-1):
	
	if flag == True:
		flag = False
		continue
	#endif
	line = lines[i]
	line2 = lines[i+1]
	
	line = line.strip().replace(' ','').replace("<spanstyle='mso-spacerun:yes'></span>",'')
	line2 = line2.strip().replace(' ','').replace("<spanstyle='mso-spacerun:yes'></span>",'')

	if len(line) == 30 and line[:9] == '<tdclass=' and line[:9] == '<tdclass=': #len('<tdclass=xl7228320>110000</td>')
		
		item = {}
		item['code'] = line[19:-5]
		item['name'] = line2[19:-5]
		
		#print(item['code'], '---' ,item['name'])
	
		blocks.append(item)
		
		flag = True
	#endif
	

#endfor



#建立树关系

adcode = []

province_map = {}
city_map = {}

for block in blocks:
	
	#如果是0000结束。则level是省
	#省/直辖市

	if block['code'][2:] == '0000' :
		province_map['name_' + block['code'][0:2]] = block['name']
		province_map['code_' + block['code'][0:2]] = block['code']
		
		item = {}
		
		item['code'] = block['code']
		item['name'] = block['name']
		item['level'] = 'province'
		
		item['name_province'] = block['name']
		item['name_city'] = ''
		item['name_county'] = ''
		item['code_province'] = block['code']
		item['code_city'] = ''
		item['code_county'] = ''
		
		adcode.append(item)
		#print('province:', item)
		
		continue
		
	#endif
	
	#如果是00结束。则level是市
	#市
	if block['code'][4:] == '00' and block['code'][2:4] != '00':
		city_map[block['code'][0:4]] = block['name']
		
		item = {}
		
		item['code'] = block['code']
		item['name'] = block['name']
		item['level'] = 'city'
		
		item['name_province'] = province_map['name_' + block['code'][0:2]]
		item['name_city'] = block['name']
		item['name_county'] = ''
		item['code_province'] = province_map['code_' + block['code'][0:2]]
		item['code_city'] = block['code']
		item['code_county'] = ''
		
		adcode.append(item)
		#print('city:', item)
		
		continue
		
	#endif
	
	#区/直辖市下属区
	if block['code'][4:] != '00' and block['code'][2:4] != '00':
		
		#如果是直辖市，直接用直辖市
		name_city = ''
		code_city = ''
		

		if 'code_' + block['code'][0:4] not in city_map:
			name_city = province_map['name_' + block['code'][0:2]]
			code_city = province_map['code_' + block['code'][0:2]]
		else:
			name_city = province_map['code_' + block['code'][0:4]]
			code_city = city_map['code_' + block['code'][0:4]]
		#endif
		

		item = {}
		
		item['code'] = block['code']
		item['name'] = block['name']
		item['level'] = 'county'
		
		item['name_province'] = province_map['name_' + block['code'][0:2]]
		item['name_city'] = name_city
		item['name_county'] = block['code']
		item['code_province'] = province_map['code_' + block['code'][0:2]]
		item['code_city'] = code_city
		item['code_county'] = block['code']
		
		adcode.append(item)
		
		#print('county:', item)
		
		continue
	#endif
	
	
#endfor


#格式化数据,转为csv或sql

for ad in adcode:
	
	line = ad['code'] + ',' + ad['name'] + ',' + ad['level'] + ',' + ad['name_province'] + ',' + ad['name_city'] + ',' + ad['name_county'] + ',' + ad['code_province'] + ',' + ad['code_city'] + ',' + ad['code_county']
	
	print(line)


#endfor























