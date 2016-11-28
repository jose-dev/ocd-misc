package com.ocado.de.osp.carrots;

import com.google.common.io.Resources;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Soil {

    private static byte[][] soil;

    public static double modifier(int xPos, int yPos) {
        byte[][] modifiers = getSoil();
        
        char modifier = (char)modifiers[xPos][yPos];
        switch(modifier) {
            case 'g':
                return 4.0;
            case 'b':
                return 2.0;
            case 'x':
                return 3.0;
        }
        return 1.0;
    }

    private static synchronized byte[][] getSoil() {
        if ( soil == null) {
            try {
                List<String> lines = Resources.readLines(Resources.getResource(Soil.class, "/shape.txt"), Charset.forName("UTF-8"));
                soil = new byte[100][100];
                for (int i = 0; i < lines.size(); i++) {
                    soil[i] = lines.get(i).getBytes();
                }
            } catch (IOException ex) {
                Logger.getLogger(Soil.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        return soil;
    }
}
