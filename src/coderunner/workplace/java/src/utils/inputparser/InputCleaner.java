package utils.inputparser;

public class InputCleaner{
    
  private String intPattern;
  private String doublePattern;
  private String intListPattern;
  private String doubleListPattern;
  private String intListsPattern;
  private String doubleListsPattern;

  public InputCleaner() {
    intPattern = "-?\\d+";
    doublePattern = "-?\\d+(\\.\\d+)?";
    intListPattern = "\\[(-?\\d+,)*(-?\\d+)?\\]";
    doubleListPattern = "\\[(-?\\d+(\\.\\d+)?,)*(-?\\d+(\\.\\d+)?)?\\]";
    intListsPattern = "\\[(\\[(-?\\d+,)*(-?\\d+)?\\],)*(\\[(-?\\d+,)*(-?\\d+)?\\])?\\]";
    doubleListsPattern = "\\[(\\[(-?\\d+(\\.\\d+)?,)*(-?\\d+(\\.\\d+)?)?\\],)*(\\[(-?\\d+(\\.\\d+)?,)*(-?\\d+(\\.\\d+)?)?\\])?\\]";
  }
  public String cleanInt(String s) {
    String str = s.replaceAll("\\s", "");
    try {
      if (!str.matches(intPattern)) {
        throw new Exception();
      }
    } catch (Exception e) {
      System.out.println("Integer Input Error!!");
      System.out.println(s);
      System.exit(0);
    }
    return str;
  }
  
  public String cleanDouble(String s) {
    String str = s.replaceAll("\\s", "");
    try {
      if (!str.matches(doublePattern)) {
        throw new Exception();
      }
    } catch (Exception e) {
      System.out.println("double Float Input Error!!");
      System.out.println(s);
      System.exit(0);
    }
    return str;
  }

  public String cleanIntList(String s) {
    String str = s.replaceAll("\\s", "");
    try {
      if (!str.matches(intPattern) && !str.matches(intListPattern)) {
        throw new Exception();
      }
    } catch (Exception e) {
      System.out.println("Integer List Input Error!!");
      System.out.println(s);
      System.exit(0);
    }
    return str;
  }

  public String cleanDoubleList(String s) {
    String str = s.replaceAll("\\s", "");
    try {
      if (!str.matches(doublePattern) && !str.matches(doubleListPattern)) {
        throw new Exception();
      }
    } catch (Exception e) {
      System.out.println("double Float List Input Error!!");
      System.out.println(s);
      System.exit(0);
    }
    return str;
  }

  public String cleanIntLists(String s) {
    String str = s.replaceAll("\\s", "");
    try {
      if (!str.matches(intPattern) && !str.matches(intListsPattern)) {
        throw new Exception();
      }
    } catch (Exception e) {
      System.out.println("List of Integer List input Error!!");
      System.out.println(s);
      System.exit(0);
    }
    return str;
  }

  public String cleanDoubleLists(String s) {
    String str = s.replaceAll("\\s", "");
    try {
      if (!str.matches(doublePattern) && !str.matches(doubleListsPattern)) {
        return str;
      } else {
        throw new Exception();
      }
    } catch (Exception e) {
      System.out.println("List of double Float List input Error!!");
      System.out.println(s);
      System.exit(0);
    }
    return str;
  }
}
