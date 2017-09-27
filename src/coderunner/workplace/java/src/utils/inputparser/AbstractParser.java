package utils.inputparser;
import java.util.ArrayList;
import java.io.BufferedReader;

public abstract class AbstractParser<S, T> {
    // variables
    protected String inputPath;
    protected BufferedReader br;
    
    // constructor
    protected AbstractParser() {}
    protected AbstractParser(String inputPath) {this.inputPath = inputPath;}

    // protected methods
    abstract protected S toValue(String str);
    abstract protected T toList(String str);
    abstract protected ArrayList<T> toLists(String str);

    // public methods
    public void setInputPath(String inputPath) {this.inputPath = inputPath;}
}