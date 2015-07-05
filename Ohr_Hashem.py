# -*- coding: utf-8 -*-
from sefaria.model import *
from sefaria.tracker import add
import urllib
import urllib2
from urllib2 import URLError, HTTPError
import json 
import pdb

def post_index(index):
	url = 'http://www.sefaria.org/api/index/' + index["title"].replace(" ", "_")
	indexJSON = json.dumps(index)
	print indexJSON
	values = {
		'json': indexJSON, 
		'apikey': 'F4J2j3RF6fHWHLtmAtOTeZHE3MOIcsgvcgtYSwMzHtM'
	}
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	try:
		response = urllib2.urlopen(req)
		print response.read()
	except HTTPError, e:
		print 'Error code: ', e.code
		
def appendNodes(root_node, subsections, key_str):
	count=0
	for sub in subsections:
	#	pdb.set_trace()
		n = JaggedArrayNode()
		n.key = "perek"+str(count)+key_str
		n.add_title(sub, "he", primary=True)
		n.add_title("Perek "+str(count+1), "en", primary=True)
		n.depth = 1
		n.sectionNames = ["Paragraph"]
		n.addressTypes = ["Integer"]
		root_node.append(n)
		count+=1



IndexSet({"title": "New Zohar"}).delete()
IndexSet({"title": "Or Hashem"}).delete()
IndexSet({"title": "Light of God"}).delete()
IndexSet({"title": u"אור השם"}).delete()
IndexSet({"title": u"אור ה'"}).delete()


root = SchemaNode()
root.add_title("Ohr Hashem", "en", primary=True)
#root.add_title("Light of God", "en", primary=False)
root.add_title(u"אור ה'", "he", primary=True)
root.key = "ohrhashem"

maamar1 = SchemaNode()
maamar1.add_title(u"המאמר הראשון", "he", primary=True)
maamar1.add_title("Ma'amar One", "en", primary=True)
maamar1.key = "m1"

m1_klal1 = SchemaNode()
m1_klal1.add_title(u"הכלל הראשון בבאור ההקדמות כפי מה שבאו מבוארות בדברי הפלוסופיס.", "he", primary=True)
m1_klal1.add_title("Section One", "en", primary=True)
m1_klal1.key = "m1 k1"
subsections_m1_k1 = [u" הפרק הא' בביאור ההקדמה הראשונה האומרת שמציאות בעל שעור אחד אין תכלית לו שקר.", 
u"הפרק הב' בבאור ההקדמה", u"הפרק הג' בבאור ההקדמה הג'", u"הפרק הד' בבאור ההקדמה הד׳",
u"הפרק הה' בבאור ההקדמה הד׳", u"הפרק הו' בבאור ההקדמה הששית", 
u"הפרק הז' בבאור ההקדמה הז׳ האומרת שכל משתנה מתחלק והוא בהכרח וכל מה שלא יתחלק לא יתנועע ולא יהיה גשם כלל.",
u"הפרק ח' בבאור ההקדמה השמינית האומרת שכל מה שיתנועע במקרה ינוח בהכרח אחר שאין תנועתו בעצמותו.",
u"הפרק ט' בבאור ההקדמה הט' דאומרת כי כל גשם שיניע גשם אמנם יגיעהו בשיתנועה גם הוא בעת הגעתו.",
u"הפרק י' בבאור ההקדמה [העשירית",
u"""הפרק י"א בבאור ההקדמה הי״א""",
u"""הפרק הי"ב בבאור ההקדמה הי״ב הפרק""",
u"""הי״ג בבאור ההקדמה הי״ג האומרת שאי אפשר שיהיה דבר ממיני השינוי מתדבק אלא תנועת ההעתק לבד והשבובית ממנה.""",
u"""הפרק י"ד בבאור הקדמה הי״ד """,
u"""הפרק ט"ו בבאור הקדמה הט"ו""",
u"""הפרק ט"ז בבאור הקדמה הט"ז""",
u"""הפרק י״ז בבאור הקדמה הי״ו""",
u"""הפרק הי״ח בבאור הקדמה הי״ח האומרת שכל מה שיצא מן הכח אל הפעל מוציאו זולתו והוא חוץ ממנו בהכרח.""",
u"""הפרק הי״ט בבאור ההקדמה היא האומרת שכל אשר למציאותו סבה הוא אפשר המציאות בבחינת עצמותו כי אם נמצאו סבותיו נמצא.""",
u"""הפרק כ' בבאור הקדמה הכ׳ האומר שכל מחוייב המציאו׳ בבחינת עצמותו הנה אין סבה למציאותו באופן מהאופנים ולא בעניין מהעניינים.""",
u"""הפרק כ״א בבאור ההקדמת הכ״א""",
u"""הפרק כ״ב בבאור ההקדמה הכ״ב האומרת שכל גשם הוא מורכב משני עניינים בהכרח וישיגהו מקרים בהכרה.""",
u"""הפרק כ"ג בבאור ההקדמה הכ"ג""",
u"""הפרק כ״ד בבאור ההקדמה הכ״ד""",
u"""הפרק כ"ה בבאור ההקדמה הכ״ה""",
u"""הפרק כ"ו בביאור ההקדמ׳ הכ״ו אשר נתנה הרב על דרך הנחה והיא האומרת שהמן והתנועה נצחיים תמדיים נמצאים בפעל.""",
u"""הפרק כ"ז בבאור המופת הראשון שיסד הרב בהקדמות אלו""",
u"""הפרק כ״ח בבאור המופת הב' אשר סדרו הרב אחר שקבל הקדמה אחת האומרת""",
u"""הפרק כ״ט בבאור המופת הג' אשר סדר הרב לקוח מדברי ארסטו""",
u"""הפרק ל' במופת הד׳ לרב וסדרו כן אנחנו נראה תמיד עניינים יוצאים מן הכח אל הפועל""",
u"""הפרק ל״א בבאור המופת הה׳ לרב בהעמיד האחדות והוא מיוחד על ההקדמה המקובל""",
u"""הפרק ל״ב בבאור המופת המשותף למאמיני הקדמות ולנו קהל המאמינים בחדוש כפי מה שסדרו הרב."""]
appendNodes(m1_klal1, subsections_m1_k1, "m1 k1")

m1_klal2 = SchemaNode()
m1_klal2.add_title(u"הכלל השני", "he", primary=True)
m1_klal2.add_title("Section Two", "en", primary=True)
m1_klal2.key = "m1 k2"
subsections_m1_k2 = [u""" פרק א נחקור בו במקצת ההקדמות ובמופתי הרב אם יתבארו באור מופתי אם לא.
הפרק הראשון נחקור בו במופתים שסדר לאמת ההקדמה הא'""",
u"""הפרק ב' בחקירה בהקדמה הב׳ האומרת שמציאות גדולים אין תכלית למספרם שקר.""",
u"""הפרק ג' בחקירה בהקדמה הג' האומרת שמציאות עלות ועלולים למספרם שקר.""",
u"""הפרק הד' בחקירה בהקדמה הזאת האומרת שכל משתנה מתחלק.""",
u"""הפרק ה' בחקירה בהקדמה האחת האומרת שכל מה שיתנועע במקרה ינוח בהכרח וזה שמה שימצא במקרה יעבור שלא ימצא כשלא יהיה מתחייב לנמצא בעצם.""",
u"""הפרק ו' בחקירה בהקדמה הט׳ האומרת כי כל גשם שיגיע גשם אמנם יניעהו בשיתנועע גם הוא בעת הנעתו.""",
u"""הפרק ז' בחקירה בהקדמה הי' האומרת כי כל מה שיאמר שהוא בגשם יחלק אל שני חלקים אם שתהיה עמידתו בגשם כמקרים.""",
u"""הפרק ח' בחקירה בהקדמה הי״ב האומרת שכל מה נמצא מתפשט בגשם""",
u"""הפרק ט׳ בחקירה בהקדמה הי״ג האומרת שאי אפשר שיהיה דבר ממיני השינוי מתדבק אלא תנועת ההעתק לבד והסבובית ממנה.""",
u"""הפרק י' בחקירה בהקדמה הי״ד האומרת שתנועת ההעתקה יותר קודמת שבתנועות והראשונה מהם בטבע""",
u"""הפרק י׳׳א בחקירה בהקדמה הי״ד האומרת שתנועת ההעתקה יותר קודמת שבתנועות והראשונה מהם בטבע""",
u"""הפרק י״ב בחקירה בהקדמה היות האומרת כי כל מה שאינו גוף לא יושכל בו מניין אלא אם יהיה כוח בגוף וימנו אישי הכחות ההם בהמנות החמרים שלהם או נושאיהם.""",
u"""הפרק י"ג בחקירה בהקדמה הכ״ב שכל גשם הוא מורכב משני עניינים בהכרח והם שני עניינים המעמידים אותו אשר הם חמרו וצורתו.""",
u"""הפרק י״ד בחקירה בהקדמה הכ״ג האומרת שכל מה שהוא בכח ולו בעצמותו אפשרות מה כבר אפשר בעת מה שלא ימצא בפעל.""",
u"""הפרק ט"ו בחקירה במופת הא' שסדרו הרב לבאר מציאות השם ואחדותו והיותו לא גשם ולא כח בו""",
u"""הפרק י״ו בחקירה המופת הב׳ שסדר הרב באלו הג' דרושים ולחקור בו ג"כ משני׳ צדדים.""",
u"""הפרק י"ז בחקירה במופת הג׳ אשר סדר הרב באלו הדרושי׳ ונחקור בו ג״כ מב׳ צדדים.""",
u"""הפרק י"ח בחקירה במופת הד׳ אשר סדר הרב באלו הדרושים ונחקור בו ג״כ משני צדדים""",
u"""הפרק י״ט בחקירה במופת הד׳ שסדר הרב באלו הדרושים ונחקור בו גם כן משני צדדים""",
u"""הפרק הכ' בחקירה במופת הו׳ המשותף למאמיני הקדמות ולנו קהל המאמינים בחודש אשר סדר הרב באלו הדרושים"""]
appendNodes(m1_klal2, subsections_m1_k2, "m1 k2")


m1_klal3 = SchemaNode()
m1_klal3.add_title(u"הכלל השלישי בבאור אלו השרשים כפי מה שגזרהו התורה מאופן עמידתנו בהם", "he", primary=True)
m1_klal3.add_title("Section Three", "en", primary=True)
m1_klal3.key = "m1 k3"
subsections_m1_k3 = [
u"הפרק א' בבאור השרש הראשון והוא מציאות השם יתברך",
u"הפרק ב' באופן עמידתנו נשרש הזה והוא לפי מה שנאמר בהקדמה הג׳ ובפרק הג׳ מהכלל השני מזה המאמר",
u"הפרק ג' בבאור השרש הב׳ והוא היותו יתברך אחד",
u"הפרק ד' באופן עמידתנו בשרש הזה",
u"הפרק ה' בבאור השרש הג׳ המונח והוא היותו י״ת לא גוף ולא כח בגוף",
u"הפרק ו' באופן עמידתנו בשרש הזה הג׳"]

appendNodes(m1_klal3, subsections_m1_k3, "m1 k3")

maamar1.append(m1_klal1)
maamar1.append(m1_klal2)
maamar1.append(m1_klal3)
 
maamar2 = SchemaNode()
maamar2.add_title(u"המאמר השני", "he", primary=True)
maamar2.add_title("Ma'amar Two", "en", primary=True)
maamar2.key = "m2" 

m2_klal1 = SchemaNode()
m2_klal1.add_title(u"הכלל הראשון בידיעת השם הנמצאות", "he", primary=True)
m2_klal1.add_title("Section One", "en", primary=True)
m2_klal1.key = "m2 k1"
subsections_m2_k1 = [u"הפרק הא׳ בבאור הפנה הזאת כפי מה שתגזרהו התורה.",
u"הפרק הב׳ בבאור הספקות שאפשר שיסופקו בהם אשר בעבורם נמעדו רגלי מקצת חכמינו ופנה הזאת.",
u"הפרק הג׳ בבאור ספקות יותר במה שחייבו בפנה הזאת.",
u"הפרק הד׳ בהתר ספקות אשר הניחו בפנה הזאת לפי דעת התורה.",
u"הפרק הה' באופן ידיעתינו בפנה הזאת בשלמות"]
appendNodes(m2_klal1, subsections_m2_k1, "m2 k1")

m2_klal2 = SchemaNode()
m2_klal2.add_title(u"הכלל השני בהשגחה", "he", primary=True)
m2_klal2.add_title("Section Two", "en", primary=True)
m2_klal2.key = "m2 k2"
subsections_m2_k2 = [u"הפרק הא' בבאור הפנה הזאת כפי מה שתגזרהו התורה:",
u"הפרק הב' בבאור הספקות שאפשר שיסופקו בה אשר בעבורם נטו מהדרך הנכון מקצת חכמינו בפנה הזאת:",
u"[הפרק הג' בבאור הספקות במה שחייבו בפנה זאת]:",
u"הפרק הד' בהתר הספקית שהניחו בפנה הזאת לפי דעת התורה:",
u"הפרק הה' באופן ידיעתינו בפנה הזאת בשלמות:",
u"הפרק הו' בבאור דרושים מתיחסים אליהם:"]
appendNodes(m2_klal2, subsections_m2_k2, "m2 k2")

m2_klal3 = SchemaNode()
m2_klal3.add_title(u"הכלל השלישי ביכולת השם", "he", primary=True)
m2_klal3.add_title("Section Three", "en", primary=True)
m2_klal3.key = "m2 k3"
subsections_m2_k3 = [u"הפרק א מאור הפנה הזאת כפי מה שתגזרהו התורה.",
						u"הפרק ב הפרק ב באור אופן ידיעתינו בפנה הזאת."]
appendNodes(m2_klal3, subsections_m2_k3, "m2 k3")	


m2_klal4 = SchemaNode()
m2_klal4.add_title(u"הכלל ד' בנבואה", "he", primary=True)
m2_klal4.add_title("Section Four", "en", primary=True)
m2_klal4.key = "m2 k4"
subsections_m2_k4 = [u"הפרק הא' בבאור שם הנבואה ועניינה כפי מה שתחייבהו התורה:",
u"הפרק ב׳ באור משיגי הנבואה העצמיים:",
u"הפרק הג׳ בהיתר ספיקות מה בנבואה כפי מה שהעידו עליהם הקודמים. ומהם שלא העידו עליהם:",
u"הפרק הד' נישיר בו אל הדין אשר תושג בו הדרגת הנבואה כפי מה אשר תגזרהו התורה ויסכים בו העיון:"]
appendNodes(m2_klal4, subsections_m2_k4, "m2 k4")

m2_klal5 = SchemaNode()
m2_klal5.add_title(u"הכלל הה׳ בבחירה", "he", primary=True)
m2_klal5.add_title("Section Five", "en", primary=True)
m2_klal5.key = "m2 k5"
subsections_m2_k5 = [u"הפרק א' הפרק א בבאור דעת מי שיראה שטבע האפשר נמצא:",
u"הפרק ב' בבאור דעת מי שיראה שטבע האפשר בלתי נמצא.",
u"הפרק ג' בבאור הדעת האמתי כפי מה שחייבהו התורה והעיון.",
u"הפרק ד' ואיך שיהיה הדעת הזה החיוב אם החיוב בבחינת הסבות או החיוב מבחנת ידיעתו יתברך:",
u"הפרק ה' נתוספת באור הדעת הזה בהתר הספק העצום הזה אשר לא סדו הקודמים להסתפק עליו:",
u"הפרק ו' בבאור מה שהתבאר בזה מצד העיון הו׳:"]
appendNodes(m2_klal5, subsections_m2_k5, "m2 k5")


m2_klal6 = SchemaNode()
m2_klal6.add_title(u"הכלל ו' בתכלית", "he", primary=True)
m2_klal6.add_title("Section Six", "en", primary=True)
m2_klal6.key = "m2 k6"
subsections_m2_k6 = [u"פרק הראשון נבאר בו התכלית האמתי בזאת התורה:",
u"השני נבאר בו איך יתאמת שיתחייב התכלית הזה מזאת התורה.",
u"הג׳ נבאר בו שהתכלית בזאת התורה היא התכלית לכלל המציאות.",
u"הד' נאמת חיוב זה מצד העיון ומהמאמרים לרז״ל.",
u"הה' נבאר שבקשת התכלית האחרון לכלל המציאות ראוי ומחויב עד שניחב בו דעת הרב:"]
appendNodes(m2_klal6, subsections_m2_k6, "m2 k6")

maamar2.append(m2_klal1)
maamar2.append(m2_klal2)
maamar2.append(m2_klal3)
maamar2.append(m2_klal4)
maamar2.append(m2_klal5)
maamar2.append(m2_klal6)
						
						
maamar3 = SchemaNode()
maamar3.add_title(u"המאמר שלישי באמונת האמתיות", "he", primary=True)
maamar3.add_title("Ma'amar Three, Part One", "en", primary=True)
maamar3.key = "m3"

m3_klal1 = SchemaNode()
m3_klal1.add_title(u"הכלל הא׳ באמונת החדוש", "he", primary=True)
m3_klal1.add_title("Section One", "en", primary=True)
m3_klal1.key = "m3 k1"
subsections_m3_k1 = [u"הפרק האחד נזכור בי טענות המפרשים לקיים הקדמות:", u"הפרק ב׳. נזכור בו תשובת הרב המורה עליהם.",
u"הג' לזכור בו מופתי הר״ל וטענותיו ותשובותיו לקיים המדרש על הדרן הנזכר.", u"הד' נברר בי הצודק מהבלתי צודק כפי מה שאפשר לנו:",
u"הה׳ נאמת בו היות דעת המדרש האמתי במה שאין ספק בו הכפירה בו הריסה בשרשי המורה ואולם איננו יסוד ופנה שלא יצוייר מציאות המורה זולתו:"]
appendNodes(m3_klal1, subsections_m3_k1, "m3 k1")

m3_klal2 = SchemaNode()
m3_klal2.add_title(u"הכלל הב׳ בהשארות הנפש", "he", primary=True)
m3_klal2.add_title("Section Two", "en", primary=True)
m3_klal2.key = "m3 k2"
subsections_m3_k2 = [u"הפרק הא' בבאור איך ראוי שיובן כפי מה שתגזרהו התורה והעיון:", u"הפרק הב׳ באופן עמידתנו עליו:"]
appendNodes(m3_klal2, subsections_m3_k2, "m3 k2")

m3_klal3 = SchemaNode()
m3_klal3.add_title(u"הכלל הג׳ בגמול וענש", "he", primary=True)
m3_klal3.add_title("Section Three", "en", primary=True)
m3_klal3.key = "m3 k3"
subsections_m3_k3 = [u"הפרק הא' בדיני הגמול והענש באופן שלא יחלוק עליו העיון:", u"הפרק הב' בבאור שני מיני הגמול ושני מיני העונש אם היה שהם מתחלפים במה זה יתחלפו:",
u"הפרק הג' בהתר קצת ספקות יקרו בשני מיני הייעוד:"]
appendNodes(m3_klal3, subsections_m3_k3, "m3 k3")


m3_klal4 = SchemaNode()
m3_klal4.add_title(u"הכלל הד׳ בתחיית המתים", "he", primary=True)
m3_klal4.add_title("Section Four", "en", primary=True)
m3_klal4.key = "m3 k4"
subsections_m3_k4 = [u"הפרק הא' בבאור הדעת הזה בעצמו:", u"הפרק הב' בתכלית המכוון בנס הנפלא הזה ותועלותיו:",
u"פרק הג' בסבות העונש המופלג למי שיכפור בשרש הזה:", u"פרק הד' בהתר קצת ספקות הנופלים בו:"]
appendNodes(m3_klal4, subsections_m3_k4, "m3 k4")


m3_klal5 = SchemaNode()
m3_klal5.add_title(u"הכלל הה׳ בנצחות התורה", "he", primary=True)
m3_klal5.add_title("Section Five", "en", primary=True)
m3_klal5.key = "m3 k5"
subsections_m3_k5 = [u"הפרק הא' אין ראוי שיובן:", u"הפרק הב' בהתר ספק שאיפשר שיסופק בשורש הזה:"]
appendNodes(m3_klal5, subsections_m3_k5, "m3 k5")

m3_klal6 = SchemaNode()
m3_klal6.add_title(u"הכלל הו׳ בהבדל שבין משה רבינו לשאר הנביאים:", "he", primary=True)
m3_klal6.add_title("Section Six", "en", primary=True)
m3_klal6.key = "m3 k6"
subsections_m3_k6 = [u"הפרק הא' במופתים:", u"הפרק הב' בעצם הנבואה:"]
appendNodes(m3_klal6, subsections_m3_k6, "m3 k6")


m3_klal7 = SchemaNode()
m3_klal7.add_title(u"הכלל הז' באורים ותומים", "he", primary=True)
m3_klal7.add_title("Section Seven", "en", primary=True)
m3_klal7.key = "m3 k7"
subsections_m3_k7 = [u"הפרק הא' בשרש הזה בעצמו:", u"הפרק הב' בהתר קצת ספקית שאיפשר שיסופקו בו:"]
appendNodes(m3_klal7, subsections_m3_k7, "m3 k7")


m3_klal8 = SchemaNode()
m3_klal8.add_title(u"הכלל הח' במשיח", "he", primary=True)
m3_klal8.add_title("Section Eight", "en", primary=True)
m3_klal8.key = "m3 k8"
subsections_m3_k8 = [u"הפרק הא' בתארי המשיח ועניינו:", u"הפרק הב׳ בזמן בואו:", u"הפרק הג' בביאור היות השרשים אשר כלל אותם המאמר הזה עם היות׳ אמתיים אין ספק באמתתם. "]
appendNodes(m3_klal8, subsections_m3_k8, "m3 k8")

maamar3.append(m3_klal1)
maamar3.append(m3_klal2)
maamar3.append(m3_klal3)
maamar3.append(m3_klal4)
maamar3.append(m3_klal5)
maamar3.append(m3_klal6)
maamar3.append(m3_klal7)
maamar3.append(m3_klal8)


maamar3b = SchemaNode()
maamar3b.add_title(u"החלק הב׳ באמונות הנתלות במצות מיוחדות", "he", primary=True)
maamar3b.add_title("Ma'amar Three, Part Two", "en", primary=True)
maamar3b.key = "m3b"

m3b_klal1 = SchemaNode()
m3b_klal1.add_title(u"הכלל הא׳ בתפלה וברכת כהנים", "he", primary=True)
m3b_klal1.add_title("Section One", "en", primary=True)
m3b_klal1.key = "m3b k1"
subsections_m3b_k1 = [u"הפרק הא׳ בתפלה:", u"הפרק הב׳ בברכת כהנים:"]
appendNodes(m3b_klal1, subsections_m3b_k1, "m3b k1")

m3b_klal2 = SchemaNode()
m3b_klal2.add_title(u"הכלל הב׳ בתשובה", "he", primary=True)
m3b_klal2.add_title("Section Two", "en", primary=True)
m3b_klal2.key = "m3b k2"
subsections_m3b_k2 = [u"הפרק הא' בביאור השרש הזה ואופן עמידתנו עליו:", u"הפרק הב' בהתר שני ספקות שאיפשר שיסופק בו"]
appendNodes(m3b_klal2, subsections_m3b_k2, "m3b k2")

m3b_klal3 = JaggedArrayNode()
m3b_klal3.add_title(u"הכלל הג׳ ביום הכפורים וד׳ פרקי השנה", "he", primary=True)
m3b_klal3.add_title("Section Three", "en", primary=True)
m3b_klal3.key = "m3b k3"
m3b_klal3.depth = 1
m3b_klal3.sectionNames = ["Paragraph"]
m3b_klal3.addressTypes = ["Integer"]

maamar3b.append(m3b_klal1)
maamar3b.append(m3b_klal2)
maamar3b.append(m3b_klal3)


maamar4 = SchemaNode()
maamar4.add_title(u"המאמר הד׳ בדעות וסברות", "he", primary=True)
maamar4.add_title("Ma'amar Four", "en", primary=True)
maamar4.key = "m4"

subsections_m4 = [u"הדרוש הא' אם העולם נצחי במה שיבא", u"הדרש הב' אם אפשר מציאות עולם אחד או עולמות רבים יחד:",
u"הדרוש הג' אם הגרמים השמימיים חיים מדברים:", u"הדרוש הד' אם יש לתנועות הנדמים השמימיים מבוא והנהגה במשפט האדם. ",
u"הדרוש הה' אם יש לקמיעות והלחשים מבוא בפעולות האדם:", u"הדרוש הששי בשדים", 
u"הדרוש הז' אם תעתק נפש האדם או תאצל והוא שיקראוהו כת מהחכמים גלגול",
u"הדרוש השמיני אם תשאר נפש הנער שאינו חייב במצות:",
u"הדרוש התשיעי בגן עדן וגהינם:",
u"הדרוש העשירי המכוון כמעשה בראשית ומעשה מרכבה ואם הוא חכמת הטבע ומה שאחריו כמו שמשכו קצת מחכמי אומתינו:",
u"הדרוש הי״א אם השכל והמשכיל והמושכל דבר אחד אם לא:",
u"הדרוש השנים עשר במניע הראשון:",
u"הדרוש השלש עשר בהמנעות השגת אמתת מהותו יתברך אם הוא מצד התורה לבד או אם יסכים בו העיון. ואם היה שיסכים בו העיון אם יש להמנעות היה טבע קיים באופן שלא יצוייד בו אפשרות: "]

count=0
for sub in subsections_m4:
	n = JaggedArrayNode()
	n.key = "drush"+str(count)+"m4"
	n.add_title(sub, "he", primary=True)
	n.add_title("Drush "+str(count+1), "en", primary=True)
	n.depth = 1
	n.sectionNames = ["Paragraph"]
	n.addressTypes = ["Integer"]
	maamar4.append(n)
	count+=1



root.append(maamar1)
root.append(maamar2)
root.append(maamar3)
root.append(maamar3b)
root.append(maamar4)
root.validate()

index = {
    "title": "Ohr Hashem",
    "categories": ["Philosophy"],
    "schema": root.serialize()
}

Index(index).save()
post_index(index)

