package org.intermine;

import java.io.*;
import org.intermine.codegen.*;
import org.intermine.metadata.*;

public class GenerateJavaModelSources
{
    public static void main(String[] args) throws Exception {
        new GenerateJavaModelSources().run(args);
    }

    public void run(String[] args) {
        if (args.length != 2)
            throw new RuntimeException("Usage: GenerateJavaModelSources <model-xml-path> <source-output-path>");

        String modelPath = args[0];
        String sourceOutputPath = args[1];

        InterMineModelParser immp = new InterMineModelParser();

        try {
            Reader r = new FileReader(modelPath);
            Model m = immp.process(r);

            JavaModelOutput jmo = new JavaModelOutput(m, new File(sourceOutputPath));
            jmo.process();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}