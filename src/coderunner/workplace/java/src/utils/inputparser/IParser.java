package utils.inputparser;
import java.util.ArrayList;

public interface IParser<S, T> {
    public void setInputPath(String inputPath);

    public ArrayList<S> parseDataAsSingleValue();
    public ArrayList<T> parseDataAsList();
    public ArrayList<ArrayList<T>> parseDataAsLists();
    //public ArrayList<ArrayList<E[][]>> parseDataAsMatrix();
}