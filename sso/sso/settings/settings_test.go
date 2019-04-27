package settings

import (
	"os"
	"testing"
)

func assertPanic(t *testing.T, f func(), msg string) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf(msg)
		}
	}()

	f()
}

func TestEnvPublicKeysKeys(t *testing.T) {
	assertPanic(t, Init, "Code did not panic on missing keys")
	os.Setenv("PRIVATE_KEY", "xxx")
	assertPanic(t, Init, "Code did not panic on missing keys")
	os.Setenv("PUBLIC_KEY", "xxx")
	Init()
}
