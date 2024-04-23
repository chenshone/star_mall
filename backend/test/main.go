package main

import (
	"fmt"

	"github.com/hashicorp/consul/api"
)

func Register(address string, port int, name string, tags []string, id string) error {
	cfg := api.DefaultConfig()
	cfg.Address = fmt.Sprintf("%s:%d", "127.0.0.1", 8500)

	client, err := api.NewClient(cfg)
	if err != nil {
		fmt.Println(err)
		return err
	}

	check := &api.AgentServiceCheck{
		HTTP:                           fmt.Sprintf("http://%s:%d/health", address, port),
		Interval:                       "10s",
		Timeout:                        "5s",
		DeregisterCriticalServiceAfter: "10s",
	}

	registration := new(api.AgentServiceRegistration)
	registration.Name = name
	registration.ID = id
	registration.Port = port
	registration.Tags = tags
	registration.Address = address
	registration.Check = check

	err = client.Agent().ServiceRegister(registration)

	if err != nil {
		fmt.Println(err)
		return err
	}

	return nil
}

func AllServices() {
	cfg := api.DefaultConfig()
	cfg.Address = "127.0.0.1:8500"

	client, err := api.NewClient(cfg)
	if err != nil {
		fmt.Println(err)
		return
	}

	services, err := client.Agent().Services()
	if err != nil {
		fmt.Println(err)
		return
	}

	for k := range services {
		fmt.Printf("%s\n", k)
	}
}

func FilterServices(service string) {
	cfg := api.DefaultConfig()
	cfg.Address = "127.0.0.1:8500"

	client, err := api.NewClient(cfg)
	if err != nil {
		fmt.Println(err)
		return
	}

	data, err := client.Agent().ServicesWithFilter(fmt.Sprintf("Service == \"%s\"", service))

	if err != nil {
		fmt.Println(err)
		return
	}

	for k := range data {
		fmt.Printf("%s\n", k)
	}
}

func main() {
	err := Register("127.0.0.1", 8021, "user-web", []string{"user-web", "user-web-1"}, "user-web")

	if err != nil {
		fmt.Println(err)
	}
}
