package utils.inputparser;
import java.util.ArrayList;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.FileReader;

public class IntegerParser extends AbstractParser<Integer,int[]> implements IParser<Integer,int[]> {
    private InputCleaner inputCleaner;
    public IntegerParser() {
        super();
        inputCleaner = new InputCleaner();
    }
    public IntegerParser(String inputPath) {
        super(inputPath);
        inputCleaner = new InputCleaner();
    }

    // protected methods
    @Override
    protected Integer toValue(String str) {
        str = inputCleaner.cleanInt(str);
        return Integer.parseInt(str);
    }

    @Override
    protected int[] toList(String str) {
        str = inputCleaner.cleanIntList(str);
        int[] output;
        if (str.charAt(0) != '[' && str.charAt(str.length() - 1) != ']') {
            output = new int[]{toValue(str)};
            return output;
        }
        str = str.substring(1, str.length() - 1);
        if (str.length() == 0) return new int[0];
        String[] input_contents = str.split(",");
        output = new int[input_contents.length];
        for (int i = 0; i < input_contents.length; i++) {
            output[i] = toValue(input_contents[i]);
        }
        return output;
    }

    @Override
    protected ArrayList<int[]> toLists(String str) {
        str = inputCleaner.cleanIntLists(str);
        ArrayList<int[]> output = new ArrayList<int[]>();
        if (str.charAt(0) != '[' && str.charAt(str.length() - 1) != ']') {
            int[] tmp = {toValue(str)};
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
    public ArrayList<Integer> parseDataAsSingleValue() {
        ArrayList<Integer> output = new ArrayList<Integer>();
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
    public ArrayList<int[]> parseDataAsList() {
        ArrayList<int[]> output = new ArrayList<int[]>();
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
    public ArrayList<ArrayList<int[]>> parseDataAsLists() {
        ArrayList<ArrayList<int[]>> output = new ArrayList<ArrayList<int[]>>();
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