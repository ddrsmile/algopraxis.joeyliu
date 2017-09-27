package utils;
import java.util.ArrayList;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.FileReader;
import utils.InputCheck;

public class InputHandler {
  // Input path String
  String inputPath;

  // Integer container
  ArrayList<Integer> inInt;
  ArrayList<int[]> inIntList;
  ArrayList<ArrayList<int[]>> inIntLists;
  ArrayList<int[][]> inIntMatrix;
  
  // double Float container 
  ArrayList<Double> inDouble;
  ArrayList<double[]> inDoubleList;
  ArrayList<ArrayList<double[]>> inDoubleLists;
  ArrayList<double[][]> inDoubleMatrix;

  // String container
  ArrayList<String> inStr;
  ArrayList<String[]> inStrList;
  ArrayList<ArrayList<String[]>> inStrLists;
  ArrayList<String[][]> inStrMatrix;

  // input file reader
  BufferedReader br;
  
  // check whether input string is numeric or not
  InputCheck IC;

  public InputHandler(String inputPath) {
    this.inputPath = inputPath;
    inInt = null;
    inIntList = null;
    inIntLists = null;
    inIntMatrix = null;
    inDouble = null;
    inDoubleList = null;
    inDoubleLists = null;
    inDoubleMatrix = null;
    inStr = null;
    inStrList = null;
    inStrLists = null;
    inStrMatrix = null;
    IC = new InputCheck();
  }

  private int getInt(String str) {
    str = IC.isInt(str);
    return Integer.parseInt(str);
  }
  
  private double getDouble(String str) {
    str = IC.isDouble(str);
    return Double.parseDouble(str);
  }
  
  private int[] getIntList(String str) {
    str = IC.isIntList(str);
    if (str.charAt(0) != '[' || str.charAt(str.length() - 1) != ']') {
      int[] tmp = {Integer.parseInt(str)};
      return tmp;
    }
    str = str.substring(1, str.length()-1);
    if (str.length() == 0) return new int[0];
    String[] ints = str.split(",");
    int[] out = new int[ints.length];
    for (int i = 0; i < ints.length; i++) {
      out[i] = Integer.parseInt(ints[i]);
    }
    return out;
  }
  
  private double[] getDoubleList(String str) {
    str = IC.isDoubleList(str);
    if (str.charAt(0) != '[' || str.charAt(str.length() - 1) != ']') {
      double[] tmp = {Double.parseDouble(str)};
      return tmp;
    }
    str = str.substring(1, str.length()-1);
    String[] doubles = str.split(",");
    double[] out = new double[doubles.length];
    for (int i = 0; i < doubles.length; i++) {
      out[i] = Double.parseDouble(doubles[i]);
    }
    return out;
  }

  private ArrayList<int[]> getIntLists(String str) {
    str = IC.isIntLists(str);
    if (str.charAt(0) != '[' || str.charAt(str.length() - 1) != ']') {
      int[] tmp = {Integer.parseInt(str)};
      ArrayList<int[]> intList = new ArrayList<int[]>();
      intList.add(tmp);
      return intList;
    }
    str = str.substring(1, str.length() - 1);
    if (str.length() == 0) return new ArrayList<int[]>();
    str = str.replace("],[", "], [");
    String[] ints = str.split(", ");
    ArrayList<int[]> intLists = new ArrayList<int[]>();
    for (int i = 0; i < ints.length; i++) {
      intLists.add(getIntList(ints[i]));
    }
    return intLists;
  }

  private ArrayList<double[]> getDoubleLists(String str) {
    str = IC.isDoubleLists(str);
    if (str.charAt(0) != '[' || str.charAt(str.length() - 1) != ']') {
      double[] tmp = {Double.parseDouble(str)};
      ArrayList<double[]> doubleList = new ArrayList<double[]>();
      doubleList.add(tmp);
      return doubleList;
    }
    str = str.substring(1, str.length() - 1);
    if (str.length() == 0) return new ArrayList<double[]>();
    str = str.replace("],[", "], [");
    String[] doubles = str.split(", ");
    ArrayList<double[]> doubleLists = new ArrayList<double[]>();
    for (int i = 0; i < doubles.length; i++) {
      doubleLists.add(getDoubleList(doubles[i]));
    }
    return doubleLists;
  }

  private String getStr(String str) {
    str = str.replace("\"","");
    return str;
  }
  
  private String[] getStrList(String str) {
    str = str.trim();
    str = str.substring(1, str.length() - 1);
    String[] strs = str.split(",");
    String[] out = new String[strs.length];
    for (int i = 0; i < strs.length; i++) {
      out[i] = strs[i].trim().replace("\"", "");
    }
    return out;
  }
  
  public ArrayList<Integer> getDataAsInt() throws IOException {
    if (inputPath == null || inputPath.length() == 0) return inInt;
    inInt = new ArrayList<Integer>();
    br = new BufferedReader(new FileReader(inputPath));
    String in = null;
    while ((in = br.readLine()) != null) {
      inInt.add(getInt(in));
    }
    return inInt;
  }
  
  public ArrayList<int[]> getDataAsIntList() throws IOException {
    if (inputPath == null || inputPath.length() == 0) return inIntList;
    inIntList = new ArrayList<int[]>();
    br = new BufferedReader(new FileReader(inputPath));
    String in = null;
    while ((in = br.readLine()) != null) {
      inIntList.add(getIntList(in));
    }
    return inIntList;
  }

  public ArrayList<ArrayList<int[]>> getDataAsIntLists() throws IOException {
    if (inputPath == null || inputPath.length() == 0) return inIntLists;
    inIntLists = new ArrayList<ArrayList<int[]>>();
    br = new BufferedReader(new FileReader(inputPath));
    String in = null;
    while ((in = br.readLine()) != null) {
      inIntLists.add(getIntLists(in));
    }
    return inIntLists;
  }

  public ArrayList<int[][]> getDataAsIntMatrix() throws IOException {
    if (inputPath == null || inputPath.length() == 0) return inIntMatrix;
    inIntMatrix = new ArrayList<int[][]>();
    br = new BufferedReader(new FileReader(inputPath));
    String in = null;
    ArrayList<int[]> tmp;
    int[][] matrix;
    while ((in = br.readLine()) != null) {
      tmp = getIntLists(in);
      int n = tmp.size();
      matrix = new int[n][];
        for (int i = 0; i < n; i++) {
          matrix[i] = tmp.get(i);
        }
      inIntMatrix.add(matrix);
    }
    return inIntMatrix;
  }

  public ArrayList<Double> getDataAsDouble() throws IOException {
    if (inputPath == null || inputPath.length() == 0) return inDouble;
    inDouble = new ArrayList<Double>();
    br = new BufferedReader(new FileReader(inputPath));
    String in = null;
    while ((in = br.readLine()) != null) {
      inDouble.add(getDouble(in));
    }
    return inDouble;
  }
 
  public ArrayList<double[]> getDataAsDoubleList() throws IOException {
    if (inputPath == null || inputPath.length() == 0) return inDoubleList;
    inDoubleList = new ArrayList<double[]>();
    br = new BufferedReader(new FileReader(inputPath));
    String in = null;
    while ((in = br.readLine()) != null) {
      inDoubleList.add(getDoubleList(in));
    }
    return inDoubleList;
  }

  public ArrayList<ArrayList<double[]>> getDataAsDoubleLists() throws IOException {
    if (inputPath == null || inputPath.length() == 0) return inDoubleLists;
    inDoubleLists = new ArrayList<ArrayList<double[]>>();
    br = new BufferedReader(new FileReader(inputPath));
    String in = null;
    while ((in = br.readLine()) != null) {
      inDoubleLists.add(getDoubleLists(in));
    }
    return inDoubleLists;
  }

  public ArrayList<double[][]> getDataAsDoubleMatrix() throws IOException {
    if (inputPath == null || inputPath.length() == 0) return inDoubleMatrix;
    inDoubleMatrix = new ArrayList<double[][]>();
    br = new BufferedReader(new FileReader(inputPath));
    String in = null;
    ArrayList<double[]> tmp;
    double[][] matrix;
    while ((in = br.readLine()) != null) {
      tmp = getDoubleLists(in);
      int n = tmp.size();
      matrix = new double[n][];
      for (int i = 0; i < n; i++) {
        matrix[i] = tmp.get(i);
      }
      inDoubleMatrix.add(matrix);
    }
    return inDoubleMatrix;
  }

  public ArrayList<String> getDataAsStr() throws IOException {
    if (inputPath == null || inputPath.length() == 0) return inStr;
    inStr = new ArrayList<String>();
    br = new BufferedReader(new FileReader(inputPath));
    String in = null;
    while ((in = br.readLine()) != null) {
      inStr.add(getStr(in));
    }
    return inStr;
  }

  public ArrayList<String[]> getDataAsStrList() throws IOException {
    if (inputPath == null || inputPath.length() == 0) return inStrList;
    inStrList = new ArrayList<String[]>();
    br = new BufferedReader(new FileReader(inputPath));
    String in = null;
    while ((in = br.readLine()) != null) {
      inStrList.add(getStrList(in));
    }
    return inStrList;
  }
}
