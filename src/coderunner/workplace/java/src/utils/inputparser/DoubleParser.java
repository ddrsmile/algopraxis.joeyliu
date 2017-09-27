package utils.inputparser;
import java.util.ArrayList;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.FileReader;

public class DoubleParser extends AbstractParser<Double,double[]> implements IParser<Double,double[]> {
    private InputCleaner inputCleaner;
    public DoubleParser() {
        super();
        inputCleaner = new InputCleaner();
    }
    public DoubleParser(String inputPath) {
        super(inputPath);
        inputCleaner = new InputCleaner();
    }

    // protected methods
    @Override
    protected Double toValue(String str) {
        str = inputCleaner.cleanDouble(str);
        return Double.parseDouble(str);
    }

    @Override
    protected double[] toList(String str) {
        str = inputCleaner.cleanDoubleList(str);
        double[] output;
        if (str.charAt(0) != '[' && str.charAt(str.length() - 1) != ']') {
            output = new double[]{toValue(str)};
            return output;
        }
        str = str.substring(1, str.length() - 1);
        if (str.length() == 0) return new double[0];
        String[] input_contents = str.split(",");
        output = new double[input_contents.length];
        for (int i = 0; i < input_contents.length; i++) {
            output[i] = toValue(input_contents[i]);
        }
        return output;
    }

    @Override
    protected ArrayList<double[]> toLists(String str) {
        str = inputCleaner.cleanDoubleLists(str);
        ArrayList<double[]> output = new ArrayList<double[]>();
        if (str.charAt(0) != '[' && str.charAt(str.length() - 1) != ']') {
            double[] tmp = {toValue(str)};
            output.add(tmp);
            return output;
        }
        str = str.substring(1, str.length() - 1);
        if (str.length() == 0) return output;
        str = str.replace("],[", "], [");
        String[] input_contents = str.split(", ");
        for (int i = 0; i < input_contents.length; i++) {
            output.add(toList(input_contents[i]));
        }
        return output;
    }
  
    @Override
    public ArrayList<Double> parseDataAsSingleValue() {
        ArrayList<Double> output = new ArrayList<Double>();
        if (inputPath == null || inputPath.length() == 0) {
            return output;
        }
        try {
            br = new BufferedReader(new FileReader(inputPath));
            String input_contents = null;
            while ((input_contents = br.readLine()) != null) {
                output.add(toValue(input_contents));
            }
        } catch (IOException ex) {
            System.out.print(ex);
        }
        return output;
    }

    @Override
    public ArrayList<double[]> parseDataAsList() {
        ArrayList<double[]> output = new ArrayList<double[]>();
        if (inputPath == null || inputPath.length() == 0) {
            return output;
        }
        try {
            br = new BufferedReader(new FileReader(inputPath));
            String input_contents = null;
            while((input_contents = br.readLine()) != null) {
                output.add(toList(input_contents));
            }
        } catch (IOException ex) {
            System.out.print(ex);
        }
        return output;
    }

    @Override
    public ArrayList<ArrayList<double[]>> parseDataAsLists() {
        ArrayList<ArrayList<double[]>> output = new ArrayList<ArrayList<double[]>>();
        if (inputPath == null || inputPath.length() == 0) {
            return output;
        }
        try {
            br = new BufferedReader(new FileReader(inputPath));
            String input_contents = null;
            while((input_contents = br.readLine()) != null) {
                output.add(toLists(input_contents));
            }
        } catch (IOException ex) {
            System.out.print(ex);
        }
        return output;
    }
}