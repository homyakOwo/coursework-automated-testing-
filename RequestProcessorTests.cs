using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace TestingDemo;

[TestClass]
public class RequestProcessorTests
{
    [TestMethod]
    public void T01_ValidApplication()
    {
        Application app = RequestProcessor.Create("U001", 2, 100m);
        Assert.AreEqual(200m, app.Total);
    }

    [TestMethod]
    public void T02_EmptyCode()
    {
        Assert.ThrowsException<ArgumentException>(
            () => RequestProcessor.Create(" ", 1, 100m));
    }

    [TestMethod]
    public void T03_NegativeQuantity()
    {
        Assert.ThrowsException<ArgumentOutOfRangeException>(
            () => RequestProcessor.Create("U003", -1, 100m));
    }

    [TestMethod]
    public void T04_MinimumQuantity()
    {
        Assert.AreEqual(10m, RequestProcessor.Create("U004", 1, 10m).Total);
    }

    [TestMethod]
    public void T05_StatusChange()
    {
        var app = RequestProcessor.Create("U005", 1, 10m);
        Assert.AreEqual("в работе", RequestProcessor.ChangeStatus(app, "в работе").Status);
    }

    [TestMethod]
    public void DiscountFiftyPercent()
    {
        Assert.AreEqual(40m, RequestProcessor.Create("U006", 1, 80m, 50m).Total);
    }

    [TestMethod]
    public void InvalidDiscountRejected()
    {
        Assert.ThrowsException<ArgumentOutOfRangeException>(
            () => RequestProcessor.Create("U007", 1, 80m, 51m));
    }
}
