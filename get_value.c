// Distributed with a free-will license.
// Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
// MMA7455
// This code is designed to work with the MMA7455_I2CS I2C Mini Module available from ControlEverything.com.
// https://www.controleverything.com/content/Accelorometer?sku=MMA7455_I2CS#tabs-0-product_tabset-2

#include <stdio.h>
#include <stdlib.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <fcntl.h>

void get_value() 
{
	// Create I2C bus
	int file;
	char *bus = "/dev/i2c-1";
	if((file = open(bus, O_RDWR)) < 0) 
	{
		printf("Failed to open the bus. \n");
		exit(1);
	}
	// Get I2C device, MMA7455 I2C address is 0x1D(29)
	ioctl(file, I2C_SLAVE, 0x1D);

// Select mode control register(0x16)
	// Measurement mode, +/- 8g(0x01)
	char config[2] = {0};
	config[0] = 0x16;
	config[1] = 0x01;
	write(file, config, 2);
	//sleep (1/2);

	// Read 6 bytes of data from register(0x00)
	// xAccl lsb, xAccl msb, yAccl lsb, yAccl msb, zAccl lsb, zAccl msb
	char reg[1] = {0x00};
	write(file, reg, 1);
	char data[6] = {0};
	if(read(file, data, 6) != 6)
		printf("Error : Input/output Error \n");
	else
	{
		// Convert the data to 10-bits
		int xAccl = ((data[1] & 0x03) * 256 + data[0]);
		if(xAccl > 511)
			xAccl -= 1024;
		int yAccl = ((data[3] & 0x03) * 256 + data[2]);
		if(yAccl > 511)
			yAccl -= 1024;
		int zAccl = ((data[5] & 0x03) * 256 + data[4]);
		if(zAccl > 511)
			zAccl -= 1024;
		// Output data to screen
		printf("X-Axis : %d \t\t", xAccl);
		printf("Y-Axis : %d \t\t", yAccl);
		printf("Z-Axis : %d \n", zAccl);
	}
}

int	main()
{
	while (1)
		get_value();
	return (0);
}
