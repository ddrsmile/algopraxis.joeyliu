package utils.inputparser;
import java.util.ArrayList;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.FileReader;

public class StringParser extends AbstractParser<String,String[]> implements IParser<String,String[]> {
    private InputCleaner inputCleaner;
    public StringParser() {
        super();
        inputCleaner = new InputCleaner();
    }
    public StringParser(String inputPath) {
        super(inputPath);
        inputCleaner = new InputCleaner();
    }
    
    @Override
    protected String toValue(String str) {
        str = str.trim().replace("\"","");
        return str;
    }

    @Override
    protected String[] toList(String str) {
        str = str.trim();
        String[] output;
        if (str.charAt(0) != '[' && str.charAt(str.length() - 1) != ']') {
            output = new String[]{toValue(str)};
            return output;
        }
        str = str.substring(1, str.length() - 1);
        if (str.length() == 0) return new String[0];
        String[] input_contents = str.split(",");
        output = new String[input_contents.length];
        for (int i = 0; i < input_contents.length; i++) {
            output[i] = toValue(input_contents[i]);
        }
        return output;
    }

    @Override
    protected ArrayList<String[]> toLists(String str) {
        str = str.trim();
        ArrayList<String[]> output = new ArrayList<String[]>();
        if (str.charAt(0) != '[' && str.charAt(str.length() - 1) != ']') {
            String[] tmp = {toValue(str)};
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
    public ArrayList<String> parseDataAsSingleValue() {
        ArrayList<String> output = new ArrayList<String>();
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
    public ArrayList<String[]> parseDataAsList() {
        ArrayList<String[]> output = new ArrayList<String[]>();
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
    public ArrayList<ArrayList<String[]>> parseDataAsLists() {
        ArrayList<ArrayList<String[]>> output = new ArrayList<ArrayList<String[]>>();
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