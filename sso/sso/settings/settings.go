package settings

import (
	"os"
	"strconv"
)

type Settings struct {
	PrivateKeyPath     string
	PublicKeyPath      string
	DatabaseHost       string
	DatabaseName       string
	DatabaseUser       string
	DatabasePassword   string
	DatabasePort       int
	JWTExpirationDelta int
}

var settings Settings = Settings{}

func Init() {
	delta, _ := strconv.Atoi(os.Getenv("EXP_DELTA"))
	db_port, _ := strconv.Atoi(os.Getenv("POSTGRES_PORT"))

	settings = Settings{
		PrivateKeyPath:     os.Getenv("PRIVATE_KEY"),
		PublicKeyPath:      os.Getenv("PUBLIC_KEY"),
		DatabaseHost:       os.Getenv("POSTGRES_HOST"),
		DatabaseName:       os.Getenv("POSTGRES_DB"),
		DatabaseUser:       os.Getenv("POSTGRES_USER"),
		DatabasePassword:   os.Getenv("POSTGRES_PASSWORD"),
		DatabasePort:       db_port,
		JWTExpirationDelta: delta,
	}

	if settings.PrivateKeyPath == "" {
		panic("Missing PRIVATE_KEY env variable")
	}

	if settings.PublicKeyPath == "" {
		panic("Missing PUBLIC_KEY env variable")
	}
}

func Get() Settings {
	if &settings == nil {
		Init()
	}

	return settings
}
