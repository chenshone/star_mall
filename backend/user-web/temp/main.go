package main

import (
	"fmt"

	"github.com/hashicorp/consul/api"
)

func Register(address string, port int, name string, tags []string, id string) (err error) {
	cfg := api.DefaultConfig()
	cfg.Address = "127.0.0.1:8500"

	client, err := api.NewClient(cfg)
	if err != nil {
		return
	}

	registration := new(api.AgentServiceRegistration)
	registration.Name = name
	registration.Port = port
	registration.Tags = tags
	registration.Address = address
	registration.ID = id

	check := &api.AgentServiceCheck{
		HTTP:                           "http://127.0.0.1:8021/health",
		Interval:                       "5s",
		Timeout:                        "3s",
		DeregisterCriticalServiceAfter: "10s",
	}
	registration.Check = check

	err = client.Agent().ServiceRegister(registration)
	if err != nil {
		return
	}

	return nil
}

func AllServices() {
	cfg := api.DefaultConfig()
	cfg.Address = "127.0.0.1:8500"

	client, err := api.NewClient(cfg)
	if err != nil {
		panic(err)
	}

	data, err := client.Agent().Services()
	if err != nil {
		panic(err)
	}

	for key := range data {
		fmt.Println(key)
	}
}

func FilterServices(name string) {
	cfg := api.DefaultConfig()
	cfg.Address = "127.0.0.1:8500"

	client, err := api.NewClient(cfg)
	if err != nil {
		panic(err)
	}

	data, err := client.Agent().ServicesWithFilter("Service == " + name)
	if err != nil {
		panic(err)
	}

	for key := range data {
		fmt.Println(key)
	}
}

func main() {
	// _ = Register("127.0.0.1", 8021, "user-web", []string{"user-web", "star_mall"}, "user-web")

	// AllServices()

	FilterServices(`"user-web"`)

}
