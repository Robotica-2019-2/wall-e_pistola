
start: TouchSensor
while not touched:
	touched = read(TouchSensor)
Stop: TouchSensor
	# outpitch, foundLove, walled, walkToMuch, sniperMode
	start: InfraSensorT, ColorSensorT, walkT
	


	walkT()
		Se outpitch:
			goBack()
			Lookback()
			outpitch=False
			walkToMuch=False
		Senão Se foundLove:
			mirar()
			atirar()
			foundLove=False
			walkToMuch=False
		Senão Se walled:
			turnAround()
			walled=False
			walkToMuch=False
		Senão Se walkToMuch:
			SniperMode()
			walkToMuch=False
		Senão:
			walk()

	InfraSensorT()
		robot = read(InfraSensor).irseek()
		Se robot[1] != None:
			foundLove=True
		Senão
			distance = read(InfraSensor).irprox()
			if distance < 20:
				walled=True
			else:
				walled=False

	ColorSensorT()

