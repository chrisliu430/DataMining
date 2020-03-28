package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"regexp"
)

func main() {
	var phoneCounter, mailCounter int
	// GET TEACHER INFO
	respTeacher, err := http.Get("http://www.csie.kuas.edu.tw/teacher.php")
	if err != nil {
		log.Fatal(err)
	}
	// GET INDEX INFO
	respIndex, err := http.Get("http://www.csie.kuas.edu.tw/index.php")
	if err != nil {
		log.Fatal(err)
	}
	// ANALYSIS BODY TAG
	unanalysisTeacherBody, err := ioutil.ReadAll(respTeacher.Body)
	unanalysisIndexBody, err := ioutil.ReadAll(respIndex.Body)
	if err != nil {
		log.Fatal(err)
	}

	strTeacher := string(unanalysisTeacherBody)
	strIndex := string(unanalysisIndexBody)

	findMail := regexp.MustCompile("[a-z].*@[a-z].*\\.tw")
	mailCounter += len(findMail.FindAllString(strTeacher, -1))
	fmt.Println(findMail.FindAllString(strTeacher, -1))
	mailCounter += len(findMail.FindAllString(strIndex, -1))
	fmt.Println(findMail.FindAllString(strIndex, -1))

	findPhone, _ := regexp.Compile("(15\\d{3})") // [^a-zA-Z]
	phoneCounter += len(findPhone.FindAllString(strTeacher, -1))
	fmt.Println(findPhone.FindAllString(strTeacher, -1))
	phoneCounter += len(findPhone.FindAllString(strIndex, -1))
	fmt.Println(findPhone.FindAllString(strIndex, -1))

	findPhone2, _ := regexp.Compile("\\(0[7,9]\\)[0-9]*.[0-9]*")
	phoneCounter += len(findPhone2.FindAllString(strTeacher, -1))
	fmt.Println(findPhone2.FindAllString(strTeacher, -1))
	phoneCounter += len(findPhone2.FindAllString(strIndex, -1))
	fmt.Println(findPhone2.FindAllString(strIndex, -1))

	fmt.Printf("Total mail number: %d\nTotal phone number: %d", mailCounter, phoneCounter)

	if err != nil {
		log.Fatal(err)
	}
}
