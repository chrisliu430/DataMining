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
	var url = [3]string{
		"http://www.csie.kuas.edu.tw/teacher.php",
		"http://www.csie.ncku.edu.tw/ncku_csie/depmember/teacher",
		"https://www.nhi.gov.tw/Content_List.aspx?n=BF3024DEFFC02A33&topn=FB01D469347C76A7"}
	// ---
	mailRule := regexp.MustCompile("[a-zA-Z0-9,.]*@[a-z,.]*")
	phoneRule, _ := regexp.Compile("\\W[0]{1,2}[0-9,-,)]{1,}[-,0-9]{3,5}[-,0-9]{3,5}")
	for idx := 0; idx < len(url); idx++ {
		resp, err := http.Get(url[idx])
		if err != nil {
			log.Fatal(err)
		}
		unAnalysisBody, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatal(err)
		}
		strBody := string(unAnalysisBody)
		fmt.Println(mailRule.FindAllString(strBody, -1), "\n", len(mailRule.FindAllString(strBody, -1)))
		fmt.Println(phoneRule.FindAllString(strBody, -1), "\n", len(phoneRule.FindAllString(strBody, -1)))
		mailCounter += len(mailRule.FindAllString(strBody, -1))
		phoneCounter += len(phoneRule.FindAllString(strBody, -1))
	}

	fmt.Printf("Total mail number: %d\nTotal phone number: %d", mailCounter, phoneCounter)
}
